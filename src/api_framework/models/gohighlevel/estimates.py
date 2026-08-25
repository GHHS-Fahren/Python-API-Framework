from pydantic import AfterValidator, AliasPath, BaseModel, ConfigDict, Field, BeforeValidator, \
    field_validator, model_validator
from datetime import datetime

from api_framework.models.common.address import FrozenAddress
from api_framework.models.common.file_models import RemoteFile
from api_framework.utils.deep_freeze import deep_freeze

from typing import Any, Annotated, Callable, Literal



estimate_statuses = Literal[
    "all", "draft", "sent", "accepted",
    "declined", "invoiced", "viewed"
]

class AddressResponse(BaseModel):
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

class EstimateBusinessResponse(BaseModel):
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
    address: AddressResponse | None
    website: str | None = None
    custom_values: tuple[CustomFieldResponse, ...] | None = None

class EstimateItemsTaxResponse(BaseModel):
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

class EstimateItemsResponse(BaseModel):
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
    taxes: tuple[EstimateItemsTaxResponse, ...]
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
    attachments: tuple[str, ...]

class EstimateDiscountResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: float | None = None
    type: Literal["percentage", "fixed"]
    valid_on_product_ids: tuple[str, ...] | None = None

class EstimateAttachmentResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    url: str
    type: str
    size: float

class EstimateContactResponse(BaseModel):
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
    address: AddressResponse | None = None
    custom_fields: Annotated[
        tuple[str, ...] | None,
        Field(validation_alias="customFields")
    ] = None

class EstimateSentToResponse(BaseModel):
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

class EstimateActionHistoryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

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
    model_config = ConfigDict(frozen=True)

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
    model_config = ConfigDict(frozen=True)

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
    model_config = ConfigDict(frozen=True)

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
        AfterValidator(lambda x: not x) # is_deleted to is_active
    ]
    name: str
    currency: str
    business: Annotated[
        EstimateBusinessResponse,
        Field(validation_alias="businessDetails")
    ]
    items: tuple[EstimateItemsResponse, ...]
    discount: EstimateDiscountResponse
    title: str | None = None
    number_prefix: Annotated[
        str | None,
        Field(validation_alias="estimateNumberPrefix")
    ] = None
    attachments: tuple[EstimateAttachmentResponse, ...]
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
        EstimateContactResponse,
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
    action_history: Annotated[
        tuple[EstimateActionHistoryResponse, ...],
        Field(validation_alias="estimateActionHistory")
    ]
    sent_to: Annotated[
        EstimateSentToResponse | None,
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
    discount_value: float
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