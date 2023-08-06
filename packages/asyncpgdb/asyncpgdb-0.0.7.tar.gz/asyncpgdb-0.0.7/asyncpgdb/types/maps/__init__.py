from typing import Optional
from typing import Union
from sqlmodel import Field
from .base import BaseSQLModel
from .base import BaseModel
from .base import TypeVar
from .base import SomeSchema
from . import util


class SQLModel(BaseSQLModel):
    @classmethod
    def tablename(cls, tablename: util.Optional[str] = None) -> str:
        return util.get_tablename(cls, tablename=tablename)

    @classmethod
    def iter_fields(cls):
        return util.iter_fields(cls)

    @classmethod
    def iter_columns(cls):
        return util.iter_columns(cls)

    @classmethod
    def primary_key(cls):
        return util.primary_key(cls)

    @classmethod
    def row2dict_serializer(cls):
        return util.get_row2dict_serializer(cls)

    @classmethod
    def row2schema_serializer(cls):
        return util.get_row2schema_serializer(cls)

    @classmethod
    def format_upsert_vars(
        cls, vars: Union[list[dict], list[SomeSchema]], include_null: bool = True
    ):
        return util.get_upsert_vars(cls, vars=vars, include_null=include_null)


class SQLSchema(BaseModel):
    @classmethod
    def tablename(cls, tablename: Optional[str] = None) -> str:
        return util.get_tablename(cls, tablename=tablename)

    @classmethod
    def iter_fields(cls):
        return util.iter_fields(cls)

    @classmethod
    def iter_columns(cls):
        return util.iter_columns(cls)

    @classmethod
    def primary_key(cls):
        return util.primary_key(cls)

    @classmethod
    def row2dict_serializer(cls):
        return util.get_row2dict_serializer(cls)

    @classmethod
    def row2schema_serializer(cls):
        return util.get_row2schema_serializer(cls)

    @classmethod
    def format_upsert_vars(
        cls, vars: Union[list[dict], list[SomeSchema]], include_null: bool = True
    ):
        return util.get_upsert_vars(cls, vars=vars, include_null=include_null)


SomeSchema = TypeVar("SomeSchema", bound=SQLSchema)
SomeModel = TypeVar("SomeModel", bound=SQLModel)
