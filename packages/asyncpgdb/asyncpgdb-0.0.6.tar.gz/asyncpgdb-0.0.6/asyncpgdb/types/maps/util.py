from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from json import loads as loadjson
from json import dumps as dumpjson
from sqlmodel import Column
from typing import Iterable
from sqlmodel.main import ModelField
from sqlmodel.main import get_column_from_field
from pydantic import BaseModel
from .base import BaseSQLModel
from .base import SomeModel
from .base import SomeSchema
from .jsonifier import JSONifier
from .jsonifier import FieldJSONifier


T = TypeVar("T")


def get(__obj: object, keys: Union[str, Iterable[str]], default: Optional[T] = None):
    if isinstance(keys, str):
        result = getattr(__obj, keys, default)
    else:
        key = next((key for key in keys if hasattr(__obj, key)), None)
        if key is None:
            result = default
        else:
            result = getattr(__obj, key, default)
    return result


def get_tablename(
    __dtype: Union[Type[SomeSchema], Type[SomeModel]], tablename: Optional[str] = None
):
    if not tablename:
        for key in ("__tablename__", "__name__"):
            if hasattr(__dtype, key):
                tablename = getattr(__dtype, key)
                break
    if tablename:
        tablename = str(tablename).lower().strip()
    return tablename


def is_primary_key(__attr: Union[Column, ModelField]):
    return (
        __attr.primary_key
        if isinstance(__attr, Column)
        else get_column_from_field(field=__attr)
    )


def iter_fields(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    return __dtype.__fields__.values()


def iter_columns(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    return (get_column_from_field(field=field) for field in iter_fields(__dtype))


def primary_key(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    pkey = next(
        (
            field
            for field in __dtype.__fields__.values()
            if get_column_from_field(field).primary_key == True
        ),
        None,
    )
    if pkey is None:
        for id_key in ("id", "uuid"):
            if id_key in __dtype.__fields__:
                pkey = __dtype.__fields__[pkey]
                break
        if not pkey:
            for id_key in ("id", "uuid"):
                pname = next(
                    (field for field in __dtype.__fields__ if field.endswith(id_key)),
                    None,
                )

                if pname:
                    pkey = __dtype.__fields__[pname]
                    break
    return pkey


def dict2schema(
    data: Dict[str, Any],
    dtype: Union[Type[SomeSchema], Type[SomeModel]],
    as_dict: bool = False,
):
    """
    Converts a dictionary to a Pydantic schema.

    :param data: The dictionary to convert.
    :param dtype: The Pydantic schema to use for the conversion.
    :return: The Pydantic schema instance created from the dictionary.
    """
    model_dict = {}

    for field in dtype.__fields__.values():
        # set the field name
        field_name = field.name

        # Get the value of the current field from the data dictionary
        field_value = data.get(field_name)

        if isinstance(field_value, str):
            if isinstance(field.type_, BaseModel):
                field_value = loadjson(field_value)
                field_value = dict2schema(field_value, field.type_)
            else:
                typename = str(field._type_display()).lower()
                if typename.startswith("dict") or typename.startswith("list"):
                    try:
                        field_value = loadjson(field_value)
                    except:
                        field_value = field_value

        # If the field value is a list, check if the list items are Pydantic models and recursively convert them
        elif isinstance(field_value, list):
            item_type = field.type_
            if issubclass(item_type, BaseModel):
                field_value = [dict2schema(item, item_type) for item in field_value]

        # Add the field value to the model dictionary
        model_dict[field_name] = field_value
    if as_dict:
        result = model_dict
    else:
        result = dtype.parse_obj(model_dict)
    # Create and return the dtype instance from the model dictionary
    return result


def get_row2dict_serializer(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    return lambda row: dict2schema(row, __dtype, as_dict=True)


def get_row2schema_serializer(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    return lambda row: dict2schema(row, __dtype)


def get_jsonifier(__dtype: Union[Type[SomeSchema], Type[SomeModel]]):
    field_jsonifiers = []
    append_field_jsonifier = field_jsonifiers.append
    for field in iter_fields(__dtype):
        name = field.name
        field_type = field.type_
        if issubclass(field_type, BaseModel) or issubclass(field_type, BaseSQLModel):
            field_type_jsonifier = get_jsonifier(field_type)
            _jsonify_field = (
                lambda value: list(map(field_type_jsonifier.jsonify, value))
                if isinstance(value, list)
                else field_type_jsonifier(value)
            )
            jsonify_field = lambda value: dumpjson(_jsonify_field(value))
        elif issubclass(field_type, dict):
            jsonify_field = lambda value: dumpjson(value)
        elif issubclass(field_type, list):
            jsonify_field = lambda value: dumpjson(value)
        else:
            jsonify_field = lambda value: value

        field_jsonifier = FieldJSONifier(name=name, jsonify=jsonify_field)
        append_field_jsonifier(field_jsonifier)
    tablename = get_tablename(__dtype)
    jsonifier = JSONifier(tablename=tablename, field_jsonifiers=field_jsonifiers)
    return jsonifier


def get_upsert_vars(
    __dtype: Union[Type[SomeSchema], Type[SomeModel]],
    vars: Union[list[dict], list[SomeSchema]],
    include_null: bool = True,
):

    jsonifier = get_jsonifier(__dtype)
    return [jsonifier.jsonify_vars(data, include_null=include_null) for data in vars]
