"""
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
       This code is out of date! Do not use for the time being!       
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
"""

from pydantic import BaseModel, field_validator, model_validator, Field, AliasPath
from datetime import datetime
from typing import Literal
from typing_extensions import Self

class SchemaField(BaseModel):
    _ACCEPTABLE_FILES = Literal[
        ".pdf", ".xlsx", ".xls", ".csv", ".jpeg",
        ".jpg", ".docx", ".doc", ".gif", ".png"
    ]

    class _Options(BaseModel):
        key: str
        label: str
        url: str|None = None

    id: str
    field_key: str
    is_standard: bool
    name: str
    type: str
    created_at: datetime
    updated_at: datetime

    options: list[_Options]|None = None
    file_formats: list[_ACCEPTABLE_FILES]|None = None
    file_limit: int|None = None

    @model_validator(mode="after")
    def validate_optionals(self) -> Self:
        if self.type in (
            "TEXTBOX_LIST", "SINGLE_OPTIONS", "MULTIPLE_OPTIONS",
            "radio select", "CHECKBOX"
        ) and not self.options:
            raise ValueError("Choice fields must define options")

        if self.type == "FILE_UPLOAD" \
        and not all(self.file_formats, self.file_limit):
            raise ValueError("File fields must define formats and limit")
        
        return self

class ObjectSchema(BaseModel):
    id: str = Field(
        validation_alias = AliasPath("object", "id")
    )
    schema_key: str = Field(
        validation_alias = AliasPath("object", "key")
    )
    labels: dict[str, str] = Field(
        validation_alias = AliasPath("object", "labels")
    )
    description: str = Field(
        validation_alias = AliasPath("object", "description")
    )
    required_fields: list[str] = Field(
        validation_alias = AliasPath("object", "requiredProperties")
    )
    created_at: datetime = Field(
        validation_alias = AliasPath("object", "createdAt")
    )
    updated_at: datetime = Field(
        validation_alias = AliasPath("object", "updatedAt")
    )
    fields: list[SchemaField] = Field(
        validation_alias = AliasPath("object", "fields")
    )

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        return datetime.fromisoformat(value)