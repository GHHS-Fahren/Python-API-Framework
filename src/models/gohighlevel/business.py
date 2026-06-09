"""
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
       This code is out of date! Do not use for the time being!       
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
"""

from pydantic import BaseModel, ConfigDict, Field, model_serializer, \
    field_validator
from datetime import datetime

from src.models.common.file_models import RemoteFile

from typing import Any



class BusinessRequest(BaseModel):
    model_config = ConfigDict(serialize_by_alias = True)

    name: str
    description: str|None = None
    phone: str|None = None
    email: str|None = None
    website: str|None = None
    address: str|None = None
    state: str|None = None
    city: str|None = None
    post_code: str|None = Field(
        default = None,
        validation_alias = "postalCode",
        serialization_alias = "postalCode"
    )
    country: str|None = None
    custom_fields: dict[str, Any]|None = Field(
        default = None,
        validation_alias = "customFields",
        serialization_alias = "customFields"
    )

class BusinessResponse(BaseModel):
    name: str
    description: str|None = None
    phone: str|None = None
    email: str|None = None
    website: str|None = None
    address: str|None = None
    state: str|None = None
    city: str|None = None
    post_code: str|None = Field(
        default = None,
        validation_alias = "postalCode"
    )
    country: str|None = None
    custom_fields: dict[str, Any]|None = Field(
        default = None,
        validation_alias = "customFields"
    )
    created_at: datetime = Field(
        validation_alias = "createdAt"
    )
    updated_at: datetime = Field(
        validation_alias = "updatedAt"
    )

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