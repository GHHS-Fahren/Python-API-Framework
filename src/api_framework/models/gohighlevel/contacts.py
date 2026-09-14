from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from pydantic.alias_generators import to_camel
from datetime import datetime, date

from typing import Annotated, Any, NotRequired, TypedDict



class ContactNoteResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    body: str
    body_text: Annotated[
        str,
        Field(validation_alias="bodyText")
    ]
    user_id: Annotated[
        str|None,
        Field(validation_alias="userId")
    ] = None
    created_at: Annotated[
        datetime,
        Field(validation_alias="dateAdded"),
        BeforeValidator(func=datetime.fromisoformat)
    ]
    contact_id: Annotated[
        str,
        Field(validation_alias="contactId")
    ]
    title: str|None = None
    colour: str|None = None
    is_pinned: Annotated[
        bool,
        Field(validation_alias="pinned")
    ]



class ContactCustomFieldResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel
    )

    id: str
    value: str

class ContactAttributionSourceResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel
    )

    url: str | None = None
    campaign: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_content: str | None = None
    referrer: str | None = None
    campaign_id: str | None = None
    fbclid: str | None = None
    gclid: str | None = None
    msclikid: str | None = None
    dclid: str | None = None
    fbc: str | None = None
    fbp: str | None = None
    fb_event_id: str | None = None
    user_agent: str | None = None
    ip: str | None = None
    medium: str | None = None
    medium_id: str | None = None

class ContactDNDConfigSettingResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel
    )

    status: str
    message: str | None = None
    code: str | None = None

class ContactDNDConfigResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel
    )

    call: ContactDNDConfigSettingResponse | None = None
    email: ContactDNDConfigSettingResponse | None = None
    sms: ContactDNDConfigSettingResponse | None = None
    whats_app: ContactDNDConfigSettingResponse | None = None
    gmb: ContactDNDConfigSettingResponse | None = None
    fb: ContactDNDConfigSettingResponse | None = None

class ContactResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel
    )

    id: str
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    email_lower_case: str | None = None
    timezone: str | None = None
    company_name: str | None = None
    phone: str | None = None
    is_dnd: Annotated[
        bool,
        Field(validation_alias="dnd")
    ]
    type: str
    source: str | None = None
    assigned_to: str | None = None
    address1: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    post_code: Annotated[
        str | None,
        Field(validation_alias="postalCode")
    ] = None
    website: str | None = None
    tags: tuple[str, ...]
    date_of_birth: date | None = None
    created_at: Annotated[
        datetime,
        Field(validation_alias="dateAdded")
    ]
    updated_at: Annotated[
        datetime,
        Field(validation_alias="dateUpdated")
    ]
    attachments: tuple[str, ...] | None = None
    # ssn <-- Literally would never need this
    keyword: str | None = None
    full_name_lower_case: str | None = None
    first_name_lower_case: str | None = None
    last_name_lower_case: str | None = None
    last_activity_at: Annotated[
        datetime | None,
        Field(validation_alias="lastActivity")
    ] = None
    custom_fields: tuple[ContactCustomFieldResponse, ...]
    business_id: str | None = None
    first_attribution_source: Annotated[
        ContactAttributionSourceResponse | None,
        Field(validation_alias="attributionSource")
    ] = None
    last_attribution_source:ContactAttributionSourceResponse|None=None
    visitor_id: str | None = None
    dnd_config: Annotated[
        ContactDNDConfigResponse | None,
        Field(validation_alias="dndSettings")
    ] = None



class ContactDndConfigSettingCreate(TypedDict):
    status: str
    message: NotRequired[str]
    code: NotRequired[str]

class ContactInboundDndConfigCreate(TypedDict):
    all: NotRequired[ContactDndConfigSettingCreate]

class ContactDndConfigCreate(TypedDict):
    call: NotRequired[ContactDndConfigSettingCreate]
    email: NotRequired[ContactDndConfigSettingCreate]
    sms: NotRequired[ContactDndConfigSettingCreate]
    whats_app: NotRequired[ContactDndConfigSettingCreate]
    gmb: NotRequired[ContactDndConfigSettingCreate]
    fb: NotRequired[ContactDndConfigSettingCreate]

class ContactCreate(TypedDict):
    name: NotRequired[str]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    email: NotRequired[str]
    timezone: NotRequired[str]
    company_name: NotRequired[str]
    phone: NotRequired[str]
    is_dnd: bool
    source: NotRequired[str]
    address1: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    country: NotRequired[str]
    post_code: NotRequired[str]
    website: NotRequired[str]
    tags: list[str]
    date_of_birth: NotRequired[date]
    custom_fields: list[dict[str, Any]]
    inbound_dnd_settings: NotRequired[ContactInboundDndConfigCreate]
    dnd_config: NotRequired[ContactDndConfigCreate]