from pydantic import BaseModel, ConfigDict, Field, AliasPath, BeforeValidator, model_validator
from datetime import datetime

from typing import Annotated, Literal, Callable, Any



class InlineAddressResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    line1: Annotated[
        str | None,
        Field(validation_alias="addressLine1")
    ] = None
    line2: Annotated[
        str | None,
        Field(validation_alias="addressLine2")
    ] = None
    city: str | None = None
    state: str | None = None
    country: Annotated[
        str | None,
        Field(validation_alias="countryCode")
    ] = None
    post_code: Annotated[
        str | None,
        Field(validation_alias="postalCode")
    ] = None


class CustomFieldResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    field_key: Annotated[
        str,
        Field(validation_alias="fieldKey")
    ]
    id: str
    value: Any

class InlineBusinessResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    logo: Annotated[
        str | None,
        Field(validation_alias="logoUrl")
    ] = None
    name: str | None = None
    phone: Annotated[
        str | None,
        Field(validation_alias="phoneNo")
    ] = None
    address: InlineAddressResponse | None
    website: str | None = None
    custom_values: tuple[CustomFieldResponse, ...] | None = None


# ============= Shared items in estimates and invoices ============= #


class InvoiceItemTaxResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    name: str
    rate: float
    calculation: Literal["exclusive"] | None = None
    description: str | None = None
    tax_id: Annotated[
        str | None,
        Field(validation_alias="taxId")
    ] = None

class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str | None, #No this is not wrong, somehow ids are not actually required
        Field(validation_alias="_id")
    ] = None
    name: str
    description: str | None = None
    product_id: Annotated[
        str | None,
        Field(validation_alias="productId")
    ] = None
    price_id: Annotated[
        str | None,
        Field(validation_alias="priceId")
    ] = None
    currency: str
    amount: float
    quantity: Annotated[
        float,
        Field(validation_alias="qty")
    ]
    taxes: tuple[InvoiceItemTaxResponse, ...]
    automatic_tax_category_id: Annotated[
        str | None,
        Field(validation_alias="automaticTaxCategoryId")
    ] = None
    is_setup_fee_item: Annotated[
        bool | None,
        Field(validation_alias="isSetupFeeItem")
    ] = None
    type: str | None = None
    is_tax_inclusive: Annotated[
        bool | None,
        Field(validation_alias="taxInclusive")
    ] = None
    attachments: tuple[str, ...] | None = None

class InvoiceDiscountResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: float | None = None
    type: Literal["percentage", "fixed"]
    valid_on_product_ids: tuple[str, ...] | None = None

class InvoiceContactResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    email_validator: Callable[
        [list[dict[str, str]]|None],
        list[str] | None
    ] =  lambda x: [i["email"] for i in x] if x is not None else None

    id: str
    name: str
    phone: Annotated[
        str | None,
        Field(validation_alias="phoneNo")
    ] = None
    email: str | None = None
    additional_emails: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="additionalEmails"),
        BeforeValidator(email_validator)
    ] = None
    company_name: Annotated[
        str | None,
        Field(validation_alias="companyName")
    ] = None
    address: InlineAddressResponse | None = None
    custom_fields: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="customFields")
    ] = None

class InvoiceAttachmentResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    url: str
    type: str
    size: float

class InvoiceSentToResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    emails: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="email")
    ] = None
    cc_emails: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="emailCc")
    ] = None
    bcc_emails: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="emailBcc")
    ] = None
    phones: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="phoneNo")
    ] = None