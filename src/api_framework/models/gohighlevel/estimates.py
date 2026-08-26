from pydantic import AfterValidator, AliasPath, BaseModel, ConfigDict, Field, BeforeValidator, \
    field_validator, model_validator
from datetime import datetime

from api_framework.models.gohighlevel.common import (
    InlineBusinessResponse, InvoiceItemResponse,
    InvoiceDiscountResponse, InvoiceAttachmentResponse,
    InvoiceContactResponse, InvoiceSentToResponse
)

from typing import Any, Annotated, Literal



estimate_statuses = Literal[
    "all", "draft", "sent", "accepted",
    "declined", "invoiced", "viewed"
]

class EstimateActionHistoryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)  # pyright: ignore[reportUnannotatedClassAttribute]

    status: Annotated[
        estimate_statuses,
        Field(validation_alias="estimateStatus")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="updatedAt")
    ]
    updated_by: Annotated[
        str | None,
        Field(validation_alias="updatedBy")
    ] = None

class EstimateFrequencySettingScheduleResponse(BaseModel):
    model_config = ConfigDict(frozen=True)  # pyright: ignore[reportUnannotatedClassAttribute]

    execute_at: Annotated[
        datetime,
        Field(validation_alias="executeAt")
    ]
    type: Annotated[
        Literal[
            "yearly", "monthly", "weekly", "daily",
            "hourly", "minutely", "secondly"
        ],
        Field(validation_alias=AliasPath(
            "rrule", "intervalType"
        ))
    ]
    interval: Annotated[
        float,
        Field(validation_alias=AliasPath(
            "rrule", "interval"
        ))
    ]
    start_at: Annotated[
        datetime,
        Field(validation_alias=AliasPath(
            "rrule", "startDatetime"
        ))
    ]
    end_at: Annotated[
        datetime | None,
        Field(validation_alias=AliasPath(
            "rrule", "endDatetime"
        ))
    ] = None
    day_of_month: Annotated[
        float | None,
        Field(validation_alias=AliasPath(
            "rrule", "dayOfMonth"
        ))
    ] = None
    day_of_week: Annotated[
        Literal["mo", "tu", "we", "th", "fr", "sa", "su"] | None,
        Field(validation_alias=AliasPath(
            "rrule", "dayOfWeek"
        ))
    ] = None
    number_of_week: Annotated[
        float | None,
        Field(validation_alias=AliasPath(
            "rrule", "numOfWeek"
        ))
    ] = None
    month_of_year: Annotated[
        Literal[
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ] | None,
        Field(validation_alias=AliasPath(
            "rrule", "monthOfYear"
        ))
    ] = None
    count: Annotated[
        float | None,
        Field(validation_alias=AliasPath(
            "rrule", "count"
        ))
    ] = None
    days_before: Annotated[
        float | None,
        Field(validation_alias=AliasPath(
            "rrule", "daysBefore"
        ))
    ] = None
    is_start_primary_user_accepted: Annotated[
        bool | None,
        Field(validation_alias=AliasPath(
            "rrule", "useStartAsPrimaryUserAccepted"
        ))
    ] = None
    end_type: Annotated[
        str | None,
        Field(validation_alias=AliasPath(
            "rrule", "endType"
        ))
    ] = None

    @model_validator(mode="before")
    @classmethod
    def merge_datetimes(
        cls,
        model_data: dict[str, str|dict[str, str|float|None]|None]
    ) -> dict[str, str|dict[str, str|float|None]|None]:
        """
        Merges the seperate `date` and `time` fields for `start` and
        `end` into one datetime field.
        """

        data = {**model_data}
        rule = {**data["rrule"]} \
            if isinstance(data["rrule"], dict) else None
        if rule is not None:
            srt_date, srt_time = rule.pop("startDate"), rule.pop("startTime")
            end_date, end_time = rule.pop("endDate"), rule.pop("endTime")
            rule["startDatetime"] = f"{srt_date}T{srt_time}" \
                if srt_time else srt_date
            rule["endDatetime"] = f"{end_date}T{end_time}" \
                if end_time else end_date
        data["rrule"] = rule
        return data

class EstimatePaymentScheduleConfig(BaseModel):
    model_config = ConfigDict(frozen=True)  # pyright: ignore[reportUnannotatedClassAttribute]

    type: str
    deposit_date_type: Annotated[
        Literal["estimate_accepted", "custom"],
        Field(validation_alias=AliasPath(
            "dateConfig", "depositDateType"
        ))
    ]
    schedule_date_type: Annotated[
        Literal["regular_interval", "custom"],
        Field(validation_alias=AliasPath(
            "dateConfig", "scheduleDateType"
        ))
    ]
    # schedules: tuple[?, ...]

class EstimateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)  # pyright: ignore[reportUnannotatedClassAttribute]

    id: Annotated[
        str,
        Field(validation_alias="_id")
    ]
    is_live: Annotated[
        bool,
        Field(validation_alias="liveMode")
    ]
    is_active: Annotated[
        bool,
        Field(validation_alias="deleted"),
        AfterValidator(lambda x: not x) # is_deleted to is_active  # pyright: ignore[reportAny]
    ]
    name: str
    currency: str
    business: Annotated[
        InlineBusinessResponse,
        Field(validation_alias="businessDetails")
    ]
    items: tuple[InvoiceItemResponse, ...]
    discount: InvoiceDiscountResponse
    title: str | None = None
    number_prefix: Annotated[
        str | None,
        Field(validation_alias="estimateNumberPrefix")
    ] = None
    attachments: tuple[InvoiceAttachmentResponse, ...]
    updated_by: Annotated[
        str | None,
        Field(validation_alias="updatedBy")
    ] = None
    total: float
    created_at: Annotated[
        datetime,
        Field(validation_alias="createdAt")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="updatedAt")
    ]
    terms: Annotated[
        str | None,
        Field(validation_alias="termsNotes")
    ] = None
    company_id: Annotated[
        str,
        Field(validation_alias="companyId")
    ]
    contact: Annotated[
        InvoiceContactResponse,
        Field(validation_alias="contactDetails")
    ]
    number: Annotated[
        float | None,
        Field(validation_alias="estimateNumber")
    ] = None
    issued_at: Annotated[
        datetime | None,
        Field(validation_alias="issueDate")
    ] = None
    expired_at: Annotated[
        datetime | None,
        Field(validation_alias="expiryDate")
    ] = None
    sent_by: Annotated[
        str | None,
        Field(validation_alias="sentBy")
    ] = None
    is_auto_taxes_calculated: Annotated[
        bool | None,
        Field(validation_alias="automaticTaxesCalculated")
    ] = None
    is_auto_taxes_enabled: Annotated[
        bool | None,
        Field(validation_alias="automaticTaxesEnabled")
    ] = None
    # meta: dict[str, Any]
    created_with_template: Annotated[
        str | None,
        Field(validation_alias=AliasPath(
            "meta", "documentCreatedByTemplateId"
        ))
    ] = None
    action_history: Annotated[
        tuple[EstimateActionHistoryResponse, ...],
        Field(validation_alias="estimateActionHistory")
    ]
    sent_to: Annotated[
        InvoiceSentToResponse | None,
        Field(validation_alias="sentTo")
    ] = None
    is_recurring: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "frequencySettings", "enabled"
        ))
    ]
    recurring_schedule: Annotated[
        EstimateFrequencySettingScheduleResponse | None,
        Field(validation_alias=AliasPath(
            "frequencySettings", "schedule"
        ))
    ] = None
    last_visited_at: Annotated[
        datetime | None,
        Field(validation_alias="lastVisitedAt")
    ] = None
    amount_in_usd: Annotated[
        float | None,
        Field(validation_alias="totalamountInUSD")
    ] = None
    is_auto_invoice_enabled: Annotated[
        bool,
        Field(validation_alias=AliasPath(
            "autoInvoice", "enabled"
        ))
    ]
    is_auto_invoice_direct_payments: Annotated[
        bool | None,
        Field(validation_alias=AliasPath(
            "autoInvoice", "directPayments"
        ))
    ] = None
    status: Annotated[
        estimate_statuses,
        Field(validation_alias="estimateStatus")
    ]
    opportunity_id: Annotated[
        str | None,
        Field(validation_alias=AliasPath(
            "opportunityDetails", "opportunityId"
        ))
    ] = None
    payment_schedule_config: Annotated[
        EstimatePaymentScheduleConfig | None,
        Field(validation_alias="paymentScheduleConfig")
    ] = None
    currency_code: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "currencyOptions", "code"
        ))
    ]
    currency_symbol: Annotated[
        str,
        Field(validation_alias=AliasPath(
            "currencyOptions", "symbol"
        ))
    ]

class EstimateTemplateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)  # pyright: ignore[reportUnannotatedClassAttribute]

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
    discount_value: float
    title: str
    name: str
    items: tuple[InvoiceItemResponse, ...]
    terms: str = Field(
        validation_alias = "termsNotes"
    )
    updated_by: str = Field(
        validation_alias = "updatedBy"
    )
    currency: str
    total: float
    # attachments: tuple[RemoteFile, ...]
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