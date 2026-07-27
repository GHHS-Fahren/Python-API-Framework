from pydantic import BaseModel, ConfigDict, Field, field_serializer, \
    field_validator
from datetime import datetime

from typing import Literal, TypedDict, NotRequired



is_none = lambda v: v is None

class CreateEmailParams(TypedDict):
    appointment_id: NotRequired[str]
    attachments: NotRequired[list[str]]
    email_from: NotRequired[str]
    email_to: NotRequired[str]
    email_cc: NotRequired[list[str]]
    email_bcc: NotRequired[list[str]]
    subject: NotRequired[str]
    html: NotRequired[str]
    email_reply_mode: NotRequired[Literal["reply", "reply_all"]]
    reply_message_id: NotRequired[str]
    template_id: NotRequired[str]
    thread_id: NotRequired[str]
    scheduled_timestamp: NotRequired[datetime]

class CreateMessageRequest(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True
    )

    type: Literal[
        "SMS", "Email", "WhatsApp", "IG", "FB",
        "Custom", "Live_Chat", "InternalComment"
    ]
    contact_id: str = Field(
        serialization_alias = "contactId"
    )
    status: Literal["delivered", "failed", "pending", "read"]
    appointment_id: str|None = Field(
        default = None,
        serialization_alias = "appointmentId",
        exclude_if = is_none
    )
    attachments: list[str]|None = Field(
        default = None,
        exclude_if = is_none
    )
    email_from: str|None = Field(
        default = None,
        serialization_alias = "emailFrom",
        exclude_if = is_none
    )
    email_to: str|None = Field(
        default = None,
        serialization_alias = "emailTo",
        exclude_if = is_none
    )
    email_cc: list[str]|None = Field(
        default = None,
        serialization_alias = "emailCc",
        exclude_if = is_none
    )
    email_bcc: list[str]|None = Field(
        default = None,
        serialization_alias = "emailBcc",
        exclude_if = is_none
    )
    html: str|None = Field(
        default = None,
        exclude_if = is_none
    )
    message: str|None = Field(
        default = None,
        exclude_if = is_none
    )
    subject: str|None = Field(
        default = None,
        exclude_if = is_none
    )
    email_reply_mode: Literal["reply", "reply_all"]|None = Field(
        default = None,
        serialization_alias = "emailReplyMode",
        exclude_if = is_none
    )
    reply_message_id: str|None = Field(
        default = None,
        serialization_alias = "replyMessageId",
        exclude_if = is_none
    )
    template_id: str|None = Field(
        default = None,
        serialization_alias = "templateId",
        exclude_if = is_none
    )
    thread_id: str|None = Field(
        default = None,
        serialization_alias = "threadId",
        exclude_if = is_none
    )
    scheduled_timestamp: datetime|None = Field(
        default = None,
        serialization_alias = "scheduledTimestamp",
        exclude_if = is_none
    )
    conversation_provider_id: str|None = Field(
        default = None,
        serialization_alias = "conversationProviderId",
        exclude_if = is_none
    )
    from_number: str|None = Field(
        default = None,
        serialization_alias = "fromNumber",
        exclude_if = is_none
    )
    to_number: str|None = Field(
        default = None,
        serialization_alias = "toNumber",
        exclude_if = is_none
    )
    mentions: list[str]|None = Field(
        default = None,
        exclude_if = is_none
    )
    user_id: str|None = Field(
        default = None,
        serialization_alias = "userId",
        exclude_if = is_none
    )

    @field_serializer("scheduled_timestamp", mode="plain")
    def serialise_timestamp(
        self,
        value: datetime
    ) -> int:
        return int(value.timestamp())

class CreateMessageResponse(BaseModel):
    model_config = ConfigDict(
        frozen = True
    )

    conversation_id: str = Field(
        validation_alias = "conversationId",
    )
    message_id: str = Field(
        validation_alias = "messageId",
    )
    email_message_id: str|None = Field(
        default = None,
        validation_alias = "emailMessageId",
    )
    message_ids: tuple[str, ...]|None = Field(
        default = None,
        validation_alias = "messageIds",
    )
    msg: str|None = Field(
        default = None,
    )

    @field_validator("message_ids", mode="before")
    @classmethod
    def validate_message_ids(
        cls,
        value: list[str]
    ) -> tuple[str, ...]:
        return tuple(value)