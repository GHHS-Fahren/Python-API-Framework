from pydantic import BaseModel, ConfigDict, Field, AliasPath, BeforeValidator, model_validator
from datetime import datetime

from api_framework.models.common.address import FrozenAddress
from api_framework.models.common.file_models import RemoteFile

from typing import Annotated



class InvoiceItemsTaxResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    tax_id: Annotated[
        str,
        Field(validation_alias="taxId")
    ]
    name: str
    rate: int
    calculation: str
    description: str

class InvoiceItemsResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    is_tax_inclusive: Annotated[
        bool,
        Field(validation_alias="taxInclusive")
    ]
    description: str
    currency: str
    product_id: Annotated[
        str,
        Field(validation_alias="productId")
    ]
    price_id: Annotated[
        str,
        Field(validation_alias="priceId")
    ]
    amount: float
    quantity: Annotated[
        float,
        Field(validation_alias="qty")
    ]
    name: str
    type: str
    taxes: tuple[InvoiceItemsTaxResponse, ...]
    attachments: tuple[RemoteFile, ...]

class InvoiceContactResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str | None = None
    phone: Annotated[
        str,
        Field(validation_alias="phoneNo")
    ] | None = None
    email: str | None = None
    additional_emails: Annotated[
        tuple[str, ...],
        Field(validation_alias="additionalEmails"),
        BeforeValidator(tuple)
    ] | None = None
    address: FrozenAddress

    @model_validator(mode="before")
    def merge_address(
        cls,
        data: dict[str, str|dict[str,str]]
    ) -> dict[str, str|dict[str,str]]:
        new_data = {**data}
        address_data: dict[str, str] = new_data.pop("address")  # pyright: ignore[reportAssignmentType]
        new_address = " ".join([
            address_data["addressLine1"]+",",
            address_data["city"],
            address_data["state"],
            address_data["postalCode"]
        ])
        return {**data, "address": {"full_address": new_address}}

class IntervalResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    interval: str
    count: Annotated[
        int,
        Field(validation_alias="intervalCount")
    ]

class InvoiceLateFeesConfigResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    is_enabled: Annotated[
        bool,
        Field(validation_alias="enable")
    ]
    type: str
    value: float
    frequency: IntervalResponse
    grace: IntervalResponse
    # charges: tuple[???, ...]
    collected_late_fees: Annotated[
        float,
        Field(validation_alias="collectedLateFees")
    ]
    total_late_fees: Annotated[
        float,
        Field(validation_alias="totalLateFees")
    ]
    max_late_fees: Annotated[
        float,
        Field(validation_alias="maxLateFees")
    ]
    # meta: dict[str, Any]


class InvoicePaymentMethodsResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    is_stripe_enabled_debit_only: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "stripe", "enableBankDebitOnly"
        ))
    ]
    is_nmi_enabled_debit_only: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "nmi", "enableBankDebitOnly"
        ))
    ]


class InvoiceSentFromResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: Annotated[
        str,
        Field(validation_alias="fromName")
    ]
    email: Annotated[
        str,
        Field(validation_alias="fromEmail")
    ]


class InvoiceSentToResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    emails: Annotated[
        tuple[str, ...],
        Field(validation_alias="email")
    ]
    cc_emails: Annotated[
        tuple[str, ...],
        Field(validation_alias="emailCc")
    ]
    bcc_emails: Annotated[
        tuple[str, ...],
        Field(validation_alias="emailBcc")
    ]


class InvoiceReminderResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    is_enabled: Annotated[
        bool,
        Field(validation_alias="enabled")
    ]
    email_template: Annotated[
        str,
        Field(validation_alias="emailTemplate")
    ]
    sms_template: Annotated[
        str,
        Field(validation_alias="smsTemplate")
    ]
    email_subject: Annotated[
        str,
        Field(validation_alias="emailSubject")
    ]
    id: Annotated[
        str,
        Field(validation_alias="reminderId")
    ]
    name: Annotated[
        str,
        Field(validation_alias="reminderName")
    ]
    time: Annotated[
        str,
        Field(validation_alias="reminderTime")
    ]
    interval_type


class InvoiceReminderSettingResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    default_email_template: str
    reminders:


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    live_mode: Annotated[
        bool,
        Field(validation_alias="liveMode")
    ]
    status: Annotated[
        str,
        Field(validation_alias="estimateStatus")
    ]
    company_id: Annotated[
        str,
        Field(validation_alias="companyId")
    ]
    discount_type: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "discount","type"
        ))
    ]
    discount_value: Annotated[
        float,
        Field(validation_alias=AliasPath(
            "discount","value"
        ))
    ]
    title: str
    name: str
    items: Annotated[
        tuple[InvoiceItemsResponse, ...],
        Field(validation_alias="invoiceItems")
    ]
    issued_at: Annotated[
        datetime,
        Field(validation_alias="issueDate"),
        BeforeValidator(datetime.fromisoformat)
    ]
    due_at: Annotated[
        datetime,
        Field(validation_alias="dueDate"),
        BeforeValidator(datetime.fromisoformat)
    ]
    terms: Annotated[
        str,
        Field(validation_alias="termsNotes")
    ]
    contact: Annotated[
        InvoiceContactResponse,
        Field(validation_alias="contactDetails")
    ]
    is_auto_taxes_calculated: Annotated[
        bool,
        Field(validation_alias="automaticTaxesCalculated")
    ]
    number: Annotated[
        str,
        Field(validation_alias="invoiceNumber")
    ]
    number_prefix: Annotated[
        str,
        Field(validation_alias="invoiceNumberPrefix")
    ]
    updated_by: Annotated[
        str,
        Field(validation_alias="updatedBy")
    ]
    currency: str
    total: float
    attachments: tuple[RemoteFile, ...]
    opportunity_id: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "opportunityDetails", "opportunityId"
        ))
    ] | None = None
    created_at: Annotated[
        datetime,
        Field(validation_alias="createdAt"),
        BeforeValidator(datetime.fromisoformat)
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="updatedAt"),
        BeforeValidator(datetime.fromisoformat)
    ]
    invoice_total: Annotated[
        float,
        Field(validation_alias="invoiceTotal")
    ]
    amount_paid: Annotated[
        float,
        Field(validation_alias="amountPaid")
    ]
    amount_due: Annotated[
        float,
        Field(validation_alias="amountDue")
    ]
    late_fees_config: Annotated[
        InvoiceLateFeesConfigResponse,
        Field(validation_alias="lateFeesConfiguration")
    ]
    # tips_percent: tuple[?, ...]
    is_tips_enabled: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "tipsConfiguration", "tipsEnabled"
        ))
    ]
    payment_methods: Annotated[
        InvoicePaymentMethodsResponse,
        Field(validation_alias="paymentMethods")
    ]
    # sync_details: tuple[?, ...]
    # tips_recieved: tuple[?, ...]
    # external_transactions: tuple[?, ...]
    last_visited_at: Annotated[
        datetime,
        Field(validation_alias="lastVisitedAt"),
        BeforeValidator(datetime.fromisoformat)
    ]
    # payment_schedule: ? | None
    is_sent: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "manualStatusTransitions", "sent"
        ))
    ]
    is_paid: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "manualStatusTransitions", "paid"
        ))
    ]
    sent_at: Annotated[
        datetime,
        Field(validation_alias="sentAt"),
        BeforeValidator(datetime.fromisoformat)
    ]
    sent_by: Annotated[
        str,
        Field(validation_alias="sentBy")
    ]
    sent_from: Annotated[
        InvoiceSentFromResponse,
        Field(validation_alias="sentFrom")
    ]
    sent_to: Annotated[
        InvoiceSentToResponse,
        Field(validation_alias="sentTo")
    ]