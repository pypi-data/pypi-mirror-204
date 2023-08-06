from __future__ import annotations

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
from shillelagh.typing import RequestedOrder

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
            table: str
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
    def parse_uri(table: str) -> Tuple[str]:
        """
        This will pass in the first n args of __init__ for the Adapter
        """
        return table

    def get_columns(self) -> Dict[str, Field]:
        return self.columns

    def run_query(self, query: str) -> Dict[str, Any]:
        return run_query(self.graphql_api, query=query, bearer_token=self.bearer_token)

    def get_data_connection(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            **kwargs: Any,
    ) -> Iterator[Dict[str, Any]]:
        fields_str = get_gql_fields(list(self.columns.keys()))
        query_args_user = dict(self.query_args)

        after = query_args_user.pop("after", None)

        # We loop for each page in the pagination
        while True:
            args = dict(query_args_user)
            if after is not None:
                args["after"] = after

            if args:
                variable_str = f"({_get_variable_argument_str(args)})"
            else:
                # Don't generate the () for empty list of args
                variable_str = ""

            if self.pagination_relay:
                page_info_str = "pageInfo {endCursor hasNextPage}"
            else:
                page_info_str = ""

            query = f"""query {{
    {self.table}{variable_str}{{
        edges{{
        node{{
            {fields_str}
        }}
        }}
        {page_info_str}
    }}
    }}"""
            query_data = self.run_query(query=query)
            query_data_connection = query_data[self.table]

            edges = query_data_connection["edges"]

            for edge in edges:
                node: Dict[str, Any] = edge["node"]

                yield {c: extract_flattened_value(node, c) for c in self.columns.keys()}

            if self.pagination_relay:
                page_info = query_data_connection["pageInfo"]
                if not page_info["hasNextPage"]:
                    break
                after = page_info["endCursor"]
            else:
                # If there is no pagination being used, break immediately
                break

    def get_data_list(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            **kwargs: Any,
    ) -> Iterator[Dict[str, Any]]:
        fields_str = get_gql_fields(list(self.columns.keys()))

        if self.query_args:
            variable_str = f"({_get_variable_argument_str(self.query_args)})"
        else:
            # Don't generate the () for empty list of query_args
            variable_str = ""

        query = f"""query {{
{self.table}{variable_str}{{
    {fields_str}
}}
}}"""
        query_data = self.run_query(query=query)
        nodes: List[Dict[str, Any]] = query_data[self.table]

        for node in nodes:
            yield {c: extract_flattened_value(node, c) for c in self.columns.keys()}

    def get_data(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            **kwargs: Any,
    ) -> Iterator[Dict[str, Any]]:
        if self.is_connection:
            return self.get_data_connection(bounds=bounds, order=order, **kwargs)
        else:
            return self.get_data_list(bounds=bounds, order=order, **kwargs)
