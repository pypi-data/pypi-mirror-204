"""Schemas dealing with the cookiecutter.desc file"""
from cookiecutter_autodocs.lib.files import dump_cookiecutter_description
from cookiecutter_autodocs.lib.files import dump_cookiecutter_json
from cookiecutter_autodocs.lib.files import load_cookiecutter_description
from cookiecutter_autodocs.lib.files import load_cookiecutter_json
from cookiecutter_autodocs.lib.typing import StrOrPath
from cookiecutter_autodocs.schemas._base import SchemaBase
from typing import Any
from typing import Dict
from typing import Optional

from pydantic import Field
from pydantic import validator


class VariableDescription(SchemaBase):
    """Schema for each entry in a cookiecutter.desc file"""

    name: str
    description: str
    default: Any
    type: Optional[str] = Field(None, description="The type of the variable")
    required: Optional[bool] = Field(None, description="Whether the variable is required or not")

    @validator("type", always=True)
    def set_type(cls, v, values):
        """Set type to the type of the default value if type is not set"""
        if v is None or v == "":
            v = type(values["default"]).__name__
        return v

    @validator("required", always=True)
    def set_required(cls, v, values):
        """Set required to True if default is empty and required is not set"""
        if v is None:
            v = values["default"] == ""
        return v

    class Config:
        """Pydantic config"""

        exclude = {"name"}


class CookieCutterDescription(SchemaBase):
    """Schema for the cookiecutter.desc file"""

    variables: Dict[str, VariableDescription]

    @property
    def cookiecutter_json(self):
        """The cookiecutter.json for this CookieCutterDescription as a dictionary"""
        return {key: value.default for key, value in self.variables.items()}

    @property
    def cookiecutter_desc_dict(self):
        """The cookiecutter.desc for this CookieCutterDescription as a dictionary"""
        return {key: value.dict() for key, value in self.variables.items()}

    @classmethod
    async def from_cookiecutter_json(cls, cookiecutter_json_path: StrOrPath) -> "CookieCutterDescription":
        """Create a CookieCutterDescription from a cookiecutter.json file"""
        cookiecutter_json: Dict[str, Any] = await load_cookiecutter_json(cookiecutter_json_path)
        return cls(
            variables={
                # mypy doesn't like that we're not passing required, but its inferred from the default value
                key: VariableDescription(
                    name=key, default=value, description="", type=type(value).__name__
                )  # type: ignore
                for key, value in cookiecutter_json.items()
            }
        )

    async def to_cookiecutter_json(self, cookiecutter_json_path: StrOrPath) -> None:
        """Write a cookiecutter.json file from the CookieCutterDescription"""
        await dump_cookiecutter_json(cookiecutter_json_path, self.cookiecutter_json)

    @classmethod
    async def from_cookiecutter_desc(cls, cookiecutter_desc_path: StrOrPath) -> "CookieCutterDescription":
        """Create a CookieCutterDescription from a cookiecutter.desc file"""
        ck_desc_dict: Dict[str, Any] = await load_cookiecutter_description(cookiecutter_desc_path)
        return cls(variables={key: VariableDescription(name=key, **value) for key, value in ck_desc_dict.items()})

    async def to_cookiecutter_desc(self, cookiecutter_desc_path: StrOrPath) -> None:
        """Write a cookiecutter.desc file from the CookieCutterDescription"""
        await dump_cookiecutter_description(cookiecutter_desc_path, self.cookiecutter_desc_dict)

    def update(self, other: "CookieCutterDescription") -> None:
        """Update the CookieCutterDescription with another CookieCutterDescription"""
        for key, value in other.variables.items():
            if key in self.variables:
                self.variables[key].default = value.default
                self.variables[key].type = value.type
                if self.variables[key].description == "" and value.description != "":
                    self.variables[key].description = value.description
            else:
                self.variables[key] = value

    def validate_cookiecutter_json(self, cookiecutter_json: Dict[str, Any], allow_empty_desc=False):
        """Validate the cookiecutter.json against the CookieCutterDescription"""
        errors = []
        for key, value in cookiecutter_json.items():
            if key not in self.variables:
                errors.append(f"Variable {key} is not in the cookiecutter.desc file")
                continue
            if not allow_empty_desc and self.variables[key].description == "":
                errors.append(f"Variable {key} has an empty description")
            if self.variables[key].type != type(value).__name__:
                errors.append(
                    f"Variable {key} has type {type(value).__name__} in cookiecutter.json, "
                    + f"but type {self.variables[key].type} in cookiecutter.desc"
                )
            if self.variables[key].default != value:
                errors.append(
                    f"Variable {key} has default {value} in cookiecutter.json, "
                    + f"but default {self.variables[key].default} in cookiecutter.desc"
                )
        for key in self.variables.keys():
            if key not in cookiecutter_json:
                errors.append(f"Variable {key} is not in the cookiecutter.json file")
        return (len(errors) == 0, errors)
