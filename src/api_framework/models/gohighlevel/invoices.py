from pydantic import BaseModel, ConfigDict, Field, AliasPath
from datetime import datetime

from api_framework.models.gohighlevel.common import (
    InlineBusinessResponse, InvoiceItemResponse,
    InvoiceDiscountResponse, InvoiceAttachmentResponse,
    InvoiceContactResponse, InvoiceSentToResponse
)

from typing import Annotated, Literal



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
        float | None,
        Field(validation_alias="maxLateFees")
    ] = None
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
        bool | None,
        Field(validation_alias=AliasPath(
            "nmi", "enableBankDebitOnly"
        ))
    ] = None

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
    # interval_type

class InvoicePaymentScheduleResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: Literal["fixed", "percentage"]
    schedules: tuple[str, ...]

# class InvoiceReminderSettingResponse(BaseModel):
#     model_config = ConfigDict(frozen=True)

#     default_email_template: str
#     reminders:

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    status: Literal[
        "draft", "sent", "payment_processing",
        "paid", "void", "partially_paid"
    ]
    is_live: Annotated[
        bool,
        Field(validation_alias="liveMode")
    ]
    amount_paid: Annotated[
        float,
        Field(validation_alias="amountPaid")
    ]
    name: str
    business: Annotated[
        InlineBusinessResponse,
        Field(validation_alias="businessDetails")
    ]
    number: Annotated[
        float,
        Field(validation_alias="invoiceNumber")
    ]
    currency: str
    contact: Annotated[
        InvoiceContactResponse,
        Field(validation_alias="contactDetails")
    ]
    issued_at: Annotated[
        datetime,
        Field(validation_alias="issueDate")
    ]
    due_at: Annotated[
        datetime,
        Field(validation_alias="dueDate")
    ]
    discount: InvoiceDiscountResponse | None = None
    items: Annotated[
        tuple[InvoiceItemResponse, ...],
        Field(validation_alias="invoiceItems")
    ]
    total: float
    title: str
    amount_due: Annotated[
        float,
        Field(validation_alias="amountDue")
    ]
    created_at: Annotated[
        datetime,
        Field(validation_alias="createdAt")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="updatedAt")
    ]
    # is_auto_taxes_enabled: Annotated[
    #     bool | None,
    #     Field(validation_alias="automaticTaxesEnabled")
    # ] = None
    is_auto_taxes_calculated: Annotated[
        bool | None,
        Field(validation_alias="automaticTaxesCalculated")
    ] = None
    payment_schedule: Annotated[
        InvoicePaymentScheduleResponse | None,
        Field(validation_alias="paymentSchedule")
    ] = None
    attachments: tuple[InvoiceAttachmentResponse, ...] | None = None
    # --- The following is completely undocumented by ghl --- #
    # Assumptions are made that it will generally follow the estimates
    company_id: Annotated[
        str,
        Field(validation_alias="companyId")
    ]
    terms: Annotated[
        str | None,
        Field(validation_alias="termsNotes")
    ] = None
    number_prefix: Annotated[
        str | None,
        Field(validation_alias="invoiceNumberPrefix")
    ] = None
    updated_by: Annotated[
        str | None,
        Field(validation_alias="updatedBy")
    ] = None
    opportunity_id: Annotated[
        str | None,
        Field(validation_alias=AliasPath(
            "opportunityDetails", "opportunityId"
        ))
    ] = None
    invoice_total: Annotated[
        float,
        Field(validation_alias="invoiceTotal")
    ]
    last_visited_at: Annotated[
        datetime | None,
        Field(validation_alias="lastVisitedAt")
    ] = None
    sent_by: Annotated[
        str | None,
        Field(validation_alias="sentBy")
    ] = None
    sent_to: Annotated[
        InvoiceSentToResponse | None,
        Field(validation_alias="sentTo")
    ] = None
    # --- The following are completely undocumented --- #
    # These are assumed from reviewing data returned from the endpoint
    late_fees_config: Annotated[
        InvoiceLateFeesConfigResponse | None,
        Field(validation_alias="lateFeesConfiguration")
    ] = None
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
    is_sent: Annotated[
        bool | None,
        Field(validation_alias=AliasPath(
            "manualStatusTransitions", "sent"
        ))
    ] = None
    is_paid: Annotated[
        bool | None,
        Field(validation_alias=AliasPath(
            "manualStatusTransitions", "paid"
        ))
    ] = None
    sent_at: Annotated[
        datetime | None,
        Field(validation_alias="sentAt")
    ] = None
    sent_from: Annotated[
        InvoiceSentFromResponse | None,
        Field(validation_alias="sentFrom")
    ] = None