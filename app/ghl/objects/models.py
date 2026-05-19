from pydantic import BaseModel, Field, model_serializer, \
    field_validator
from datetime import datetime

from app.core.file_models import RemoteFile

from typing import Any



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
    custom_fields: dict[str, Any]|None = Field(
        validation_alias="properties", default=None
    )
    relations: list[dict]|None = None

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
    ) -> dict[str, Any]:
        """
        Scans for any fields that could be files and convert them
        to a remote file object
        """
        custom_fields = {}
        for name, value in fields.items():
            if not isinstance(value, dict):
                custom_fields[name] = value
            elif ("meta" in value) and ("url" in value):
                # custom field is likely a file so parse it
                custom_fields[name] = [
                    RemoteFile.model_validate({
                        "name": file["meta"]["name"],
                        "url": file["url"]
                    }) for file in value
                ]
            else:
                custom_fields[name] = value
        return custom_fields