from __future__ import annotations


import time
import dateutil.parser

import requests
from shillelagh.fields import DateTime, Field, Float, Order, Integer
from collections import defaultdict
from typing import (
    Any,
    Collection,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)
from urllib.parse import parse_qs, urlparse

from shillelagh.adapters.base import Adapter
from shillelagh.fields import (
    Boolean,
    Field,
    Filter,
    Float,
    Integer,
    ISODate,
    ISODateTime,
    ISOTime,
    String,
)
from shillelagh.typing import RequestedOrder, Row

from .lib import get_last_query, run_query
from .types import TypedDict


# -----------------------------------------------------------------------------


class MaybeNamed(TypedDict):
    name: Optional[str]


class TypeInfo(MaybeNamed):
    ofType: Optional[Union[TypeInfo, MaybeNamed]]
    # technically an enum:
    kind: str


class FieldInfo(TypedDict):
    name: str
    type: TypeInfo


class TypeInfoWithFields(TypeInfo):
    fields: Optional[List[FieldInfo]]


QueryArg = Union[str, int]


# -----------------------------------------------------------------------------


def parse_gql_type(type_info: TypeInfo) -> Field:
    # TODO(cancan101): do we want to handle Nones here?
    name: Optional[str] = type_info["name"]
    if name == "String":
        return String()
    elif name == "ID":
        # TODO(cancan101): figure out if we want to map this to UUID, int, etc
        # This should probably be an API-level setting
        return String()
    elif name == "Int":
        return Integer()
    elif name == "Float":
        return Float()
    elif name == "Boolean":
        return Boolean()
    # These are extended scalars:
    elif name == "DateTime":
        # https://www.graphql-scalars.dev/docs/scalars/date-time
        return ISODateTime()
    elif name == "Date":
        # https://www.graphql-scalars.dev/docs/scalars/date
        return ISODate()
    elif name == "Time":
        # https://www.graphql-scalars.dev/docs/scalars/time
        return ISOTime()
    else:
        # TODO(cancan101): how do we want to handle other scalars?
        raise ValueError(f"Unknown type: {name}")


def get_type_entries(
        field_obj: FieldInfo,
        *,
        data_types: Dict[str, TypeInfoWithFields],
        include: Collection[str],
        path: Optional[List[str]] = None,
) -> Dict[str, Field]:
    path = path or []

    field_name = field_obj["name"]
    new_path = path + [field_name]

    field_obj_type = field_obj["type"]

    kind = field_obj_type["kind"]
    if kind == "SCALAR":
        field_field = parse_gql_type(field_obj_type)
        return {"__".join(new_path): field_field}
    elif kind == "NON_NULL":
        of_type = field_obj_type["ofType"]

        if of_type is None:
            raise ValueError("of_type is None")

        of_type_name = of_type["name"]
        if of_type_name is None:
            raise ValueError("of_type_name is None")

        return get_type_entries(
            FieldInfo(
                name=field_name,
                type=data_types[of_type_name],
            ),
            data_types=data_types,
            include=include,
            path=path,
        )
    # TODO(cancan101): other types to handle:
    # LIST, ENUM, UNION, INTERFACE, OBJECT (implicitly handled)
    else:
        # Check to see if this is a requested include
        if field_name in include:
            ret = {}
            name = field_obj_type["name"]
            if name is None:
                raise ValueError(f"Unable to get type of: {field_name}")

            fields = data_types[name]["fields"]
            if fields is None:
                raise ValueError(f"Unable to get fields for: {name}")

            for field in fields:
                ret.update(
                    get_type_entries(
                        field, data_types=data_types, include=include, path=new_path
                    )
                )
            return ret

        return {}


# -----------------------------------------------------------------------------


# clean these up:
def find_by_name(name: str, *, types: List[FieldInfo]) -> Optional[FieldInfo]:
    name_match = [x for x in types if x["name"] == name]
    if len(name_match) == 0:
        return None
    return name_match[0]


def find_type_by_name(name: str, *, types: List[FieldInfo]) -> Optional[TypeInfo]:
    entry = find_by_name(name, types=types)
    if entry is None:
        return None
    return entry["type"]


def get_edges_type_name(fields: List[FieldInfo]) -> Optional[str]:
    entry_type = find_type_by_name("edges", types=fields)
    if entry_type is None:
        return None
    edges_info = entry_type["ofType"]
    if edges_info is None:
        return None
    return edges_info["name"]


def get_node_type_name(fields: List[FieldInfo]) -> Optional[str]:
    node_info = find_type_by_name("node", types=fields)
    if node_info is None:
        return None
    return node_info["name"]


# -----------------------------------------------------------------------------


def extract_flattened_value(node: Dict[str, Any], field_name: str) -> Any:
    ret: Any = node
    for path in field_name.split("__"):
        if ret is None:
            return ret
        elif not isinstance(ret, dict):
            raise TypeError(f"{field_name} is not dict path")
        ret = ret.get(path)
    return ret


def get_gql_fields(column_names: Sequence[str]) -> str:
    # TODO(cancan101): actually nest this
    def get_field_str(fields: List[str], root: Optional[str] = None) -> str:
        ret = " ".join(fields)
        if root is not None:
            ret = f"{root} {{{ret}}}"
        return ret

    mappings: Dict[Optional[str], List[str]] = defaultdict(list)
    for field in [x.split("__", 1) for x in column_names]:
        if len(field) == 1:
            mappings[None].append(field[-1])
        else:
            mappings[field[0]].append(field[-1])

    fields_str = " ".join(
        get_field_str(fields, root=root) for root, fields in mappings.items()
    )
    return fields_str


def _parse_query_arg(k: str, v: List[str]) -> Tuple[str, str]:
    if len(v) > 1:
        raise ValueError(f"{k} was specified {len(v)} times")

    return (k, v[0])


def _parse_query_args(query: Dict[str, List[str]]) -> Dict[str, QueryArg]:
    str_args = dict(
        _parse_query_arg(k[4:], v) for k, v in query.items() if k.startswith("arg_")
    )
    int_args = dict(
        (k, int(v))
        for k, v in (
            _parse_query_arg(k[5:], v)
            for k, v in query.items()
            if k.startswith("iarg_")
        )
    )
    overlap = set(str_args.keys()) & set(int_args.keys())
    if overlap:
        raise ValueError(f"{overlap} was specified in multiple arg sets")

    return dict(str_args, **int_args)


def _format_arg(arg: QueryArg) -> str:
    if isinstance(arg, str):
        return f'"{arg}"'
    return str(arg)


def _get_variable_argument_str(args: Dict[str, QueryArg]) -> str:
    return " ".join(f"{k}: {_format_arg(v)}" for k, v in args.items())


# -----------------------------------------------------------------------------


class GraphQLAdapter(Adapter):
    safe = True

    def __init__(
        self,
        table: str,
        include: Collection[str],
        query_args: Dict[str, QueryArg],
        is_connection: bool,
        graphql_api: str,
        bearer_token: Optional[str] = None,
        pagination_relay: Optional[bool] = None,
    ):
        super().__init__()

        print("初始化我了system")
        self._set_columns()



    def _set_columns(self) -> None:
        self.columns: Dict[str, Field] = {
            "timestamp": DateTime(filters=None, order=Order.ASCENDING, exact=False),
            "value": Integer(filters=None,
                             order=Order.NONE,
                             exact=False, )
        }

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        # TODO the slow path here could connect to the GQL Server
        return True

    @staticmethod
    def parse_uri(table: str) -> Tuple[str, List[str], Dict[str, QueryArg], bool]:
        """
        This will pass in the first n args of __init__ for the Adapter
        """
        parsed = urlparse(table)
        query_string = parse_qs(parsed.query)

        include_entry = query_string.get("include")
        is_connection = get_last_query(query_string.get("is_connection", "1")) != "0"

        include: List[str] = []
        if include_entry:
            for i in include_entry:
                include.extend(i.split(","))

        query_args = _parse_query_args(query_string)

        return (parsed.path, include, query_args, is_connection)

    def get_columns(self) -> Dict[str, Field]:
        return self.columns

    def get_data(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs: Any,
    ) -> Iterator[Row]:

        login_url = "https://sso.axa-dev.wise-paas.top/v4.0/auth/native"
        login_response = requests.post(login_url, json={"username": "admin@advantech.com.cn", "password": "Cherry@123"})
        login_result = login_response.json()

        url = "https://portal-apm-bemsdev-cluster01.axa-dev.wise-paas.top/api-apm/api/v1/hist/raw/data"
        params = {
            "sensors": [
                {
                    "nodeId": 8600,
                    "sensorType": "UsageAnalysis",
                    "sensorName": "Daily 电_EC"
                }
            ],
            "startTs": "2012-12-31T16:00:00.000Z",
            "endTs": "2022-12-31T16:00:00.000Z",
            "count": 9999,
            "retTsType": "unixTs"
        }
        cookies = {'EIToken': login_result['accessToken']}
        response = requests.post(url, json=params, cookies=cookies)
        payload = response.json()
        ##datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", value['ts']),'%Y-%m-%d %H:%M:%S'),
        for record in payload:
            for value in record['value']:
                yield {
                    "timestamp": dateutil.parser.parse(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value['ts']/1000))),
                    "value": value['v']
                }
