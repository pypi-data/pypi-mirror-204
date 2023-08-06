from typing import Type
from typing import TypeVar
from sqlmodel import SQLModel as BaseSQLModel
from sqlmodel.main import BaseModel

SomeSchema = TypeVar("SomeSchema", bound=BaseModel)
SomeModel = TypeVar("SomeModel", bound=BaseSQLModel)

DataType = Type[SomeSchema or SomeModel]
