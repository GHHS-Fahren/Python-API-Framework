from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



class CompanyContactResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True
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
    first_name: str = Field(
        validation_alias = "first"
    )
    last_name: str = Field(
        validation_alias = "last"
    )
    mobile: str
    phone: str
    email: str

# DEPRECIATED
"""
 - ready_to_invoice
 - ready_to_invoice_stamp
 - active_network_request_uuid
 - related_knowledge_articles
"""