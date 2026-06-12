from pydantic import BaseModel, ConfigDict, Field, model_serializer, \
    field_validator
from datetime import datetime
from types import MappingProxyType

from api_framework.models.common.file_models import RemoteFile
from api_framework.models.common.ghl_contact \
    import EmbeddedContactResponse
from api_framework.utils.deep_freeze import deep_freeze

from typing import Mapping, TypedDict, Optional, Any



class EstimateItemsTaxResponse(BaseModel):
    id: str = Field(
        serialization_alias = "_id"
    )
    tax_id: str = Field(
        serialization_alias = "taxId"
    )
    name: str
    rate: str
    calculation: str
    description: str

class EstimateItemsResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        serialization_alias = "_id"
    )
    tax_inclusive: bool = Field(
        serialization_alias = "tax_inclusive"
    )
    description: str
    currency: str
    product_id: str = Field(
        serialization_alias = "productId"
    )
    price_id: str = Field(
        serialization_alias = "priceId"
    )
    amount: int
    quantity: int = Field(
        serialization_alias = "qty"
    )
    name: str
    type: str
    taxes: tuple[EstimateItemsTaxResponse, ...]
    attachments: tuple[RemoteFile, ...]

class EstimateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        serialization_alias = "_id"
    )
    live_mode: bool = Field(
        serialization_alias = "liveMode"
    )
    is_deleted: bool = Field(
        serialization_alias = "deleted"
    )
    status: str = Field(
        serialization_alias = "estimateStatus"
    )
    company_id: str = Field(
        serialization_alias = "companyId"
    )
    discount: Mapping[str, Any]
    title: str
    name: str
    items: tuple[EstimateItemsResponse, ...]
    issue_date: datetime = Field(
        serialization_alias = "issueDate"
    )
    expiry_date: datetime = Field(
        serialization_alias = "expiryDate"
    )
    terms: str = Field(
        serialization_alias = "termsNotes"
    )
    contact: EmbeddedContactResponse = Field(
        serialization_alias = "contactDetails"
    )
    automatic_taxes_calculated: bool = Field(
        serialization_alias = "automaticTaxesCalculated"
    )
    meta: Mapping[str, Any]
    number: int = Field(
        serialization_alias = "estimateNumber"
    )
    number_prefix: str = Field(
        serialization_alias = "estimateNumberPrefix"
    )
    updated_by: str = Field(
        serialization_alias = "updatedBy"
    )
    currency: str
    action_history: tuple[Any, ...] = Field(
        serialization_alias = "estimateActionHistory"
    )
    frequency_settings: Mapping[str, Any] = Field(
        serialization_alias = "frequencySettings"
    )
    total: int
    attachments: tuple[RemoteFile, ...]
    auto_invoice: Mapping[str, Any] = Field(
        serialization_alias = "autoInvoice"
    )
    opportunity_details: Mapping[str, Any] = Field(
        serialization_alias = "opportunityDetails"
    )
    configuration: Mapping[str, Any]
    created_at: datetime = Field(
        serialization_alias = "createdAt"
    )
    updated_at: datetime = Field(
        serialization_alias = "updatedAt"
    )
    currency_options: Mapping[str, Any] = Field(
        serialization_alias = "currencyOptions"
    )

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
        "discount", "contact",
        "meta", "action_history",
        "frequency_settings", "auto_invoice",
        "opportunity_details", "configuration",
        "currency_options"
    )
    @classmethod
    def validate_freezable(
        cls,
        value
    ) -> Any:
        return deep_freeze(value)


class EstimateTemplateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(
        serialization_alias = "_id"
    )
    live_mode: bool = Field(
        serialization_alias = "liveMode"
    )
    is_deleted: bool = Field(
        serialization_alias = "deleted"
    )
    discount: Mapping[str, Any]
    title: str
    name: str
    items: tuple[EstimateItemsResponse, ...]
    terms: str = Field(
        serialization_alias = "termsNotes"
    )
    updated_by: str = Field(
        serialization_alias = "updatedBy"
    )
    currency: str
    total: int
    attachments: tuple[RemoteFile, ...]
    configuration: Mapping[str, Any]
    created_at: datetime = Field(
        serialization_alias = "createdAt"
    )
    updated_at: datetime = Field(
        serialization_alias = "updatedAt"
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
    
    @field_validator(
        "discount", "configuration",
        mode = "before"
    )
    @classmethod
    def validate_freezable(
        cls,
        value
    ) -> Any:
        return deep_freeze(value)