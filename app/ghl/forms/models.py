from pydantic import BaseModel, ConfigDict, AliasPath, Field, \
    model_validator, field_validator, field_serializer
from datetime import datetime

from app.core.file_models import RemoteFile

from typing import Literal, Self, overload, Any



class FormFields():
    def __init__(
        self,
        fields: dict[str, Any],
        index_map: list[str],
        name_map: dict[str, str]|None = None
    ) -> None:
        for name, value in fields.items():
            fields[name] = self._parse_field(value)
        self._fields = fields
        self._index_map = index_map
        self._name_map = name_map or {}

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
    
    def get_by_name(self, field_name: str) -> Any:
        """Retrieves a field by the field name"""
        return self._fields[self._name_map[field_name]]

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
    model_config = ConfigDict(arbitrary_types_allowed = True)

    id: str
    contact_id: str = Field(
        validation_alias = "contactId"
    )
    form_id: str = Field(
        validation_alias = "formId"
    )
    submission_id: str = Field(
        validation_alias = AliasPath("others", "submissionId")
    )
    created_at: datetime = Field(
        validation_alias = "createdAt"
    )
    attribution: dict[str, Any] = Field(
        validation_alias = AliasPath("others", "eventData")
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
