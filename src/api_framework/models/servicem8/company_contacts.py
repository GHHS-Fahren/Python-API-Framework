from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

from api_framework.utils.model_validations import model_del_empty_str

from typing import Any



class CompanyContactResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True,
    )

    id: str = Field(
        validation_alias = "uuid"
    )
    company_id: str = Field(
        validation_alias = "company_uuid"
    )
    is_active: bool = Field(
        validation_alias = "active"
    )
    is_primary_contact: bool
    type: str
    updated_at: datetime = Field(
        validation_alias = "edit_date"
    )
    first_name: str|None = Field(
        validation_alias = "first",
        default = None
    )
    last_name: str|None = Field(
        validation_alias = "last",
        default = None
    )
    mobile: str|None = None
    phone: str|None = None
    email: str|None = None

    @model_validator(mode="before")
    @classmethod
    def del_empty_str(cls, data) -> dict[str, Any]:
        return model_del_empty_str(data)