from pydantic import BaseModel, ConfigDict, Field, model_serializer, \
    field_validator
from datetime import datetime
from types import MappingProxyType

from api_framework.models.common.file_models import RemoteFile
from api_framework.utils.deep_freeze import deep_freeze

from typing import Mapping, TypedDict, Optional, Any



def is_file(data: Any) -> bool:
    if not isinstance(data, dict): return False
    return ("meta" in data) and ("url" in data)

def field_to_files(data: list[dict]) -> list[RemoteFile]:
    return [
        RemoteFile.model_validate({
            "name": file["meta"]["name"],
            "url": file["url"]
        }) for file in data
    ]

class CustomObjectParams(TypedDict):
    owners: Optional[list[str]]
    followers: Optional[list[str]]
    custom_fields: Optional[dict[str, Any]]

class CustomObjectRequest(BaseModel):
    owners: list[str]|None = None
    followers: list[str]|None = None
    custom_fields: dict[str, Any]|None = Field(
        default = None,
        validation_alias = "properties"
    )

    @model_serializer(mode="plain")
    def serialise(
        self
    ) -> dict:
        """
        Converts the object to a dictionary that conforms to the
        api requirements
        """
        data = {}
        if self.owners: data["owners"] = self.owners
        if self.followers: data["followers"] = self.followers
        if self.custom_fields: data["properties"] = self.custom_fields
        return data

class CustomObjectResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True
    )

    id: str
    object_id: str = Field(
        validation_alias = "objectId"
    )
    object_key: str = Field(
        validation_alias = "objectKey"
    )
    created_at: datetime = Field(
        validation_alias = "createdAt"
    )
    updated_at: datetime = Field(
        validation_alias = "updatedAt"
    )
    custom_fields: Mapping[str, Any]|None = Field(
        validation_alias="properties", default=None
    )
    relations: tuple[Mapping, ...]|None = None

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        """
        Converts the date fields to a datetime object
        """
        return datetime.fromisoformat(value)
    
    @field_validator("custom_fields", mode="before")
    @classmethod
    def validate_custom_fields(
        cls,
        fields: dict[str, Any]
    ) -> MappingProxyType[str, Any]:
        """
        Scans for any fields that could be files and convert them
        to a remote file object
        """
        custom_fields = {}
        for name, value in fields.items():
            if isinstance(value, list):
                if is_file(value[0]):
                    custom_fields[name] = field_to_files(value)
                else:
                    custom_fields[name] = value
            else:
                custom_fields[name] = value
        return {
            k: deep_freeze(v)
            for k,v in custom_fields.items()
        }
    
    @field_validator("relations", mode="before")
    @classmethod
    def validate_relations(
        cls,
        value: list[dict]
    ) -> tuple[MappingProxyType, ...]:
        return tuple([
            deep_freeze(i)
            for i in value
        ])