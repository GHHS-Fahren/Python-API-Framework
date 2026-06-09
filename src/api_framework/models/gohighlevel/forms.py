from pydantic import BaseModel, ConfigDict, AliasPath, Field, \
    model_validator, field_validator, field_serializer
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

from api_framework.models.common.file_models import RemoteFile
from api_framework.utils.deep_freeze import deep_freeze

from typing import Literal, Self, Mapping, overload, Any



@dataclass(frozen=True, init=False)
class FormFields:
    _fields: Mapping[str, Any]
    _index_map: tuple[str, ...]
    _name_map: Mapping[str, Any]

    def __init__(
        self,
        fields: dict[str, Any],
        index_map: list[str],
        name_map: dict[str, str]|None = None
    ) -> None:
        object.__setattr__(
            self,
            "_fields",
            MappingProxyType({
                k: deep_freeze(self._parse_field(v))
                for k,v in fields.items()
            })
        )

        object.__setattr__(
            self,
            "_index_map",
            tuple(index_map)
        )

        object.__setattr__(
            self,
            "_name_map",
            MappingProxyType(name_map or {})
        )

    @staticmethod
    def _parse_field(
        field: Any
    ) -> Any:
        if not isinstance(field, dict):
            return field
        first_value = next(iter(field.values()))
        if (
            isinstance(first_value, dict)
            and "meta" in first_value
            and "url" in first_value
        ):
            return [
                RemoteFile.model_validate({
                    "name": file["meta"]["originalname"],
                    "mime": file["meta"]["mimetype"],
                    "url": file["url"]
                }) for file in field.values()
            ]
        else:
            return field

    def set_name_map(
        self,
        name_mappings: dict[str, str]
    ) -> None:
        """Sets the name mappings"""
        self._name_map = name_mappings
    
    def get_by_id(self, field_id: str) -> Any:
        """Retrieves a field by the internal id"""
        return self._fields[field_id]
    
    def get_by_index(self, field_index: int) -> Any:
        """Retrieves a field by the question number"""
        return self._fields[self._index_map[field_index]]
    
    def get_by_name(self, field_name: str) -> Any|None:
        """
        Retrieves a field by the field name. Requires `_name_map` to
        be set.

        If `field_name` has a valid name map but does not exist in the
        fields it will return `None` as it could be an optional field
        that just wasnt filled in the form.
        """
        field_id = self._name_map[field_name]
        return self._fields.get(field_id, None)

    @overload
    def get_all(self, mapping: Literal["INDEX"]) -> list[Any]: ...
    @overload
    def get_all(self, mapping: Literal["NAME"]) -> dict[Any]: ...
    @overload
    def get_all(self, mapping: Literal["ID"]) -> dict[Any]: ...

    def get_all(
        self,
        mapping: Literal["INDEX", "NAME", "ID"]
    ):
        """
        Retrieves all form fields and returns one of:
         - "INDEX": list in order of form questions.
         - "NAME": dictionary keyed by `name_map`.
         - "ID": dictionary keyed by internal id.
        
        Will throw `ValueError` if `mapping` is invalid.
        """
        if mapping == "ID":
            return self._fields
        elif mapping == "INDEX":
            return [
                self._fields[field_id]
                for field_id in self._index_map
            ]
        elif mapping == "NAME":
            return {
                field_name: self._fields[field_id]
                for field_name, field_id in self._name_map.items()
            }
        raise ValueError(mapping)
    
    def __str__(self) -> str:
        return str(self.get_all("NAME"))

class FormSubmissionResponse(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        frozen = True
    )

    id: str
    contact_id: str = Field(
        validation_alias = "contactId",
    )
    form_id: str = Field(
        validation_alias = "formId",
    )
    submission_id: str = Field(
        validation_alias = AliasPath("others", "submissionId"),
    )
    created_at: datetime = Field(
        validation_alias = "createdAt",
    )
    attribution: Mapping[str, Any] = Field(
        validation_alias = AliasPath("others", "eventData"),
    )
    fields: FormFields

    @model_validator(mode="before")
    @classmethod
    def validate_responses(
        cls,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        index_map = [
            id for id in data["others"]["fieldsOriSequance"]
            if id in data["others"]
        ]
        fields = {
            k: v for (k,v) in data["others"].items()
            if k in index_map
        }
        return {
            **data,
            "fields": FormFields(
                fields, index_map, data.get("name_map", None)
            )
        }
    
    @field_validator("created_at", mode="before")
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        return datetime.fromisoformat(value)
    
    @field_validator("attribution", mode="before")
    @classmethod
    def validate_attribution(
        cls,
        value: dict[str, Any]
    ) -> MappingProxyType[str, Any]:
        return MappingProxyType({
            k: deep_freeze(v)
            for k,v in value.items()
        })

    @classmethod
    def model_validate_with_names(
        cls,
        data: dict[str, Any],
        name_map: dict[str, str] = None
    ) -> Self:
        return cls.model_validate({**data, "name_map": name_map})
    
    @field_serializer("fields", mode="plain")
    def serialise_fields(
        self,
        fields: FormFields
    ) -> dict[str, Any]:
        return fields.get_all("ID")
