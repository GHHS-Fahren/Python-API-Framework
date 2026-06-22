from pydantic import BaseModel, ConfigDict, Field, BeforeValidator, \
    field_validator, model_validator
from datetime import datetime

from api_framework.models.common.address import FrozenAddress
from api_framework.models.common.file_models import RemoteFile
from api_framework.utils.deep_freeze import deep_freeze

from collections.abc import Mapping
from typing import Any, Annotated



class EstimateItemsTaxResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        validation_alias = "_id"
    )
    tax_id: str = Field(
        validation_alias = "taxId"
    )
    name: str
    rate: int
    calculation: str
    description: str

class EstimateItemsResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        validation_alias = "_id"
    )
    tax_inclusive: bool = Field(
        validation_alias = "taxInclusive"
    )
    description: str
    currency: str
    product_id: str = Field(
        validation_alias = "productId"
    )
    price_id: str = Field(
        validation_alias = "priceId"
    )
    amount: int
    quantity: int = Field(
        validation_alias = "qty"
    )
    name: str
    type: str
    taxes: tuple[EstimateItemsTaxResponse, ...]
    attachments: tuple[RemoteFile, ...]

class EstimateContactResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    phone: str = Field(
        validation_alias = "phoneNo"
    )
    email: str
    additional_emails: Annotated[
        tuple[str, ...],
        BeforeValidator(tuple)
    ] = Field(
        validation_alias = "additionalEmails"
    )
    address: FrozenAddress
    # This is a dict of an unknown format so it has to be disabled
    # otherwise the hashable tests fail, hasbnt been used once in a
    # request of 200 invoices soooooo
    # custom_fields: Annotated[
    #     tuple[Any, ...],
    #     BeforeValidator(deep_freeze)
    # ] = Field(
    #     validation_alias = "customFields"
    # )

class EstimateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        validation_alias = "_id"
    )
    live_mode: bool = Field(
        validation_alias = "liveMode"
    )
    is_deleted: bool = Field(
        validation_alias = "deleted"
    )
    status: str = Field(
        validation_alias = "estimateStatus"
    )
    company_id: str = Field(
        validation_alias = "companyId"
    )
    # discount: Mapping[str, Any]
    discount_type: str
    discount_value: int
    title: str
    name: str
    items: tuple[EstimateItemsResponse, ...]
    issue_date: datetime = Field(
        validation_alias = "issueDate"
    )
    expiry_date: datetime = Field(
        validation_alias = "expiryDate"
    )
    terms: str = Field(
        validation_alias = "termsNotes"
    )
    contact: EstimateContactResponse = Field(
        validation_alias = "contactDetails"
    )
    automatic_taxes_calculated: bool = Field(
        validation_alias = "automaticTaxesCalculated"
    )
    # meta: Mapping[str, Any]
    created_with_template: str|None
    number: int = Field(
        validation_alias = "estimateNumber"
    )
    number_prefix: str = Field(
        validation_alias = "estimateNumberPrefix"
    )
    updated_by: str = Field(
        validation_alias = "updatedBy"
    )
    currency: str
    action_history: tuple[Any, ...] = Field(
        validation_alias = "estimateActionHistory"
    )
    # frequency_settings: Mapping[str, Any] = Field(
    #     validation_alias = "frequencySettings"
    # )
    total: int
    attachments: tuple[RemoteFile, ...]
    # auto_invoice: Mapping[str, Any] = Field(
    #     validation_alias = "autoInvoice"
    # )
    # opportunity_details: Mapping[str, Any] = Field(
    #     validation_alias = "opportunityDetails"
    # )
    opportunity_id: str|None = None
    # configuration: Mapping[str, Any]
    created_at: datetime = Field(
        validation_alias = "createdAt"
    )
    updated_at: datetime = Field(
        validation_alias = "updatedAt"
    )
    # currency_options: Mapping[str, Any] = Field(
    #     validation_alias = "currencyOptions"
    # )

    @field_validator(
        "created_at", "updated_at",
        "issue_date", "expiry_date",
        mode="before"
    )
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        """
        Converts the date fields to a datetime object
        """
        return datetime.fromisoformat(value)
    
    @field_validator(
        "action_history",
        mode="before"
    )
    @classmethod
    def validate_freezable(
        cls,
        value
    ) -> Any:
        return deep_freeze(value)
    
    @model_validator(mode="before")
    @classmethod
    def flatten_data(
        cls,
        model_data: dict[str, Any]
    ) -> dict[str, Any]:
        new_data = {**model_data}
        new_data["created_with_template"] = new_data["meta"]["documentCreatedByTemplateId"]
        if new_data["opportunityDetails"]:
            new_data["opportunity_id"] = new_data["opportunityDetails"]["opportunityId"]
        new_data["discount_type"] = new_data["discount"]["type"]
        new_data["discount_value"] = new_data["discount"]["value"]
        return new_data


class EstimateTemplateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        validation_alias = "_id"
    )
    live_mode: bool = Field(
        validation_alias = "liveMode"
    )
    is_deleted: bool = Field(
        validation_alias = "deleted"
    )
    discount_type: str
    discount_value: int
    title: str
    name: str
    items: tuple[EstimateItemsResponse, ...]
    terms: str = Field(
        validation_alias = "termsNotes"
    )
    updated_by: str = Field(
        validation_alias = "updatedBy"
    )
    currency: str
    total: int
    attachments: tuple[RemoteFile, ...]
    # configuration: Mapping[str, Any]
    created_at: datetime = Field(
        validation_alias = "createdAt"
    )
    updated_at: datetime = Field(
        validation_alias = "updatedAt"
    )

    @field_validator(
        "created_at", "updated_at",
        mode="before"
    )
    @classmethod
    def validate_dates(
        cls,
        value: str
    ) -> datetime:
        """
        Converts the date fields to a datetime object
        """
        return datetime.fromisoformat(value)
    
    @model_validator(mode="before")
    @classmethod
    def flatten_data(
        cls,
        model_data: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            **model_data,
            "discount_type": model_data["discount"]["type"],
            "discount_value": model_data["discount"]["value"]
        }