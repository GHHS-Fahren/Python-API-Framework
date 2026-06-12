from pydantic import BaseModel, ConfigDict, Field, model_validator, \
    field_validator
from datetime import datetime
from typing import TypedDict, Literal, Any

from api_framework.models.common.address import FrozenAddress



class JobResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True
    )

    id: str = Field(
        validation_alias = "uuid"
    )
    number: int = Field(
        validation_alias = "generated_job_id"
    )
    is_active: bool = Field(
        validation_alias = "active"
    )
    created_by: str|None = Field(
        validation_alias = "created_by_staff_uuid",
        default = None
    )
    company: str|None = Field(
        validation_alias = "company_uuid",
        default = None
    )
    category: str|None = Field(
        validation_alias = "category_uuid",
        default = None
    )
    queue: str|None = Field(
        validation_alias = "queue_uuid",
        default = None
    )
    queue_assigned_staff: str|None = Field(
        validation_alias = "queue_assigned_staff_uuid",
        default = None
    )
    completed_by: str|None = Field(
        validation_alias = "completion_actioned_by_uuid",
        default = None
    )
    payment_by: str|None = Field(
        validation_alias = "payment_actioned_by_uuid",
        default = None
    )
    created_at: datetime|None = Field(
        validation_alias = "created_at",
        default = None
    )
    status: Literal[
        "Quote", "Work Order", "Unsuccessful", "Completed"
    ]
    address: FrozenAddress # convert multifields into one
    is_address_valid: bool|None = Field(
        validation_alias = "geo_is_valid",
        default = None
    )
    billing_address: str|None = None
    description: str|None = Field(
        validation_alias = "job_description",
        default = None
    )
    work_done: str|None = Field(
        validation_alias = "work_done_description",
        default = None
    )
    badges: tuple[str, ...]|None = None
    updated_at: datetime|None = Field(
        validation_alias = "edit_date",
        default = None
    )
    quoted_at: datetime|None = Field(
        validation_alias = "quote_date",
        default = None
    )
    is_quote_sent: bool|None = Field(
        validation_alias = "quote_sent",
        default = None
    )
    quote_sent_at: datetime|None = Field(
        validation_alias = "quote_sent_stamp",
        default = None
    )
    invoice_amount: float|None = Field(
        validation_alias = "total_invoice_amount",
        default = None
    )
    purchase_order_number: str|None = None
    is_invoice_sent: bool|None = Field(
        validation_alias = "invoice_sent",
        default = None
    )
    invoice_sent_at: datetime|None = Field(
        validation_alias = "invoice_sent_stamp",
        default = None
    )
    payment_method: str|None = None
    payment_amount: float|None = None
    payment_note: str|None = None
    payment_at: datetime|None = Field(
        validation_alias = "payment_date",
        default = None
    )
    is_payment_processed: bool|None = Field(
        validation_alias = "payment_processed",
        default = None
    )
    payment_processed_at: datetime|None = Field(
        validation_alias = "payment_processed_stamp",
        default = None
    )
    is_payment_recieved: bool|None = Field(
        validation_alias = "payment_recieved",
        default = None
    )
    payment_recieved_at: datetime|None = Field(
        validation_alias = "payment_recieved_stamp",
        default = None
    )
    work_order_at: datetime|None = Field(
        validation_alias = "work_order_stamp",
        default = None
    )
    queue_expires_at: datetime|None = Field(
        validation_alias = "queue_expiry_date",
        default = None
    )
    scheduled_end_at: datetime|None = Field(
        validation_alias = "job_is_scheduled_until_stamp",
        default = None
    )
    completed_at: datetime|None = Field(
        validation_alias = "completion_date",
        default = None
    )
    unsuccessful_at: datetime|None = Field(
        validation_alias = "unsuccessful_date",
        default = None
    )

    @model_validator(mode="before")
    @classmethod
    def validate_address(
        cls,
        model_data: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            **model_data,
            "address": FrozenAddress.model_validate({
                "latitude": model_data.get("lat", None),
                "longitude": model_data.get("lng", None),
                "number": model_data.get("geo_number", None),
                "street": model_data.get("geo_street", None),
                "city": model_data.get("geo_city", None),
                "state": model_data.get("geo_state", None),
                "postcode": model_data.get("geo_postcode", None),
                "country": model_data.get("geo_country", None),
                "full_address": model_data.get("job_address", None)
            })
        }

    @field_validator(
        "created_at", "updated_at", "quoted_at",
        "quote_sent_at", "invoice_sent_at",
        "payment_at", "payment_processed_at",
        "payment_recieved_at", "work_order_at",
        "queue_expires_at", "scheduled_end_at",
        "completed_at", "unsuccessful_at",
        mode = "before"
    )
    @classmethod
    def validate_dates(
        cls,
        date: str
    ) -> datetime:
        return datetime.fromisoformat(date)

    @field_validator(
        "is_address_valid", "is_quote_sent",
        "is_invoice_sent", "is_payment_processed",
        "is_payment_recieved", "is_active",
        mode = "before"
    )
    @classmethod
    def validate_bools(
        cls,
        boolean: str
    ) -> bool:
        return boolean == "1"
    
    @field_validator(
        "number",
        mode = "before"
    )
    @classmethod
    def validate_number(
        cls,
        number: str
    ) -> int:
        return int(number)
    
    @field_validator(
        "invoice_amount", "payment_amount",
        mode = "before"
    )
    @classmethod
    def validate_amounts(
        cls,
        amount: str
    ) -> float:
        return float(amount)