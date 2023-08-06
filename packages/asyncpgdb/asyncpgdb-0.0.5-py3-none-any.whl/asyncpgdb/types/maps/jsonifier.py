import json
from typing import Any
from typing import Callable
from typing import Union
from pydantic import BaseModel
from pydantic import BaseConfig
from .base import SomeModel
from .base import SomeSchema


class FieldJSONifier(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    name: str
    jsonify: Callable[[Any], Any]


class JSONifier(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    tablename: str
    field_jsonifiers: list[FieldJSONifier]

    def jsonify_dict(self, __data: Union[dict, SomeModel, SomeSchema]):
        getter = dict.__getitem__ if isinstance(__data, dict) else getattr
        return {
            field.name: field.jsonify(value)
            for (field, value) in (
                (field, getter(__data, field.name)) for field in self.field_jsonifiers
            )
        }

    def jsonify_vars(
        self, __data: Union[dict, SomeModel, SomeSchema], include_null: bool = True
    ):
        getter = dict.get if isinstance(__data, dict) else getattr
        vars = []
        for field in self.field_jsonifiers:
            name = field.name
            value = getter(__data, name, None)
            if value is None:
                if include_null:
                    vars.append(value)
            else:
                jvalue = field.jsonify(value)

                vars.append(jvalue)
        return tuple(vars)
