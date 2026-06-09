from pydantic import BaseModel, ConfigDict, Field, field_serializer, \
    field_validator
from datetime import datetime

from typing import Literal, Optional, TypedDict, Any



is_none = lambda v: v is None

class CreateEmailParams(TypedDict):
    appointment_id: Optional[str]
    attachments: Optional[list[str]]
    email_from: Optional[str]
    email_to: Optional[str]
    email_cc: Optional[list[str]]
    email_bcc: Optional[list[str]]
    subject: Optional[str]
    html: Optional[str]
    email_reply_mode: Optional[Literal["reply", "reply_all"]]
    reply_message_id: Optional[str]
    template_id: Optional[str]
    thread_id: Optional[str]
    scheduled_timestamp: Optional[datetime]

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
    appointment_id: Optional[str] = Field(
        default = None,
        serialization_alias = "appointmentId",
        exclude_if = is_none
    )
    attachments: Optional[list[str]] = Field(
        default = None,
        exclude_if = is_none
    )
    email_from: Optional[str] = Field(
        default = None,
        serialization_alias = "emailFrom",
        exclude_if = is_none
    )
    email_to: Optional[str] = Field(
        default = None,
        serialization_alias = "emailTo",
        exclude_if = is_none
    )
    email_cc: Optional[list[str]] = Field(
        default = None,
        serialization_alias = "emailCc",
        exclude_if = is_none
    )
    email_bcc: Optional[list[str]] = Field(
        default = None,
        serialization_alias = "emailBcc",
        exclude_if = is_none
    )
    html: Optional[str] = Field(
        default = None,
        exclude_if = is_none
    )
    message: Optional[str] = Field(
        default = None,
        exclude_if = is_none
    )
    subject: Optional[str] = Field(
        default = None,
        exclude_if = is_none
    )
    email_reply_mode: Optional[Literal["reply", "reply_all"]] = Field(
        default = None,
        serialization_alias = "emailReplyMode",
        exclude_if = is_none
    )
    reply_message_id: Optional[str] = Field(
        default = None,
        serialization_alias = "replyMessageId",
        exclude_if = is_none
    )
    template_id: Optional[str] = Field(
        default = None,
        serialization_alias = "templateId",
        exclude_if = is_none
    )
    thread_id: Optional[str] = Field(
        default = None,
        serialization_alias = "threadId",
        exclude_if = is_none
    )
    scheduled_timestamp: Optional[datetime] = Field(
        default = None,
        serialization_alias = "scheduledTimestamp",
        exclude_if = is_none
    )
    conversation_provider_id: Optional[str] = Field(
        default = None,
        serialization_alias = "conversationProviderId",
        exclude_if = is_none
    )
    from_number: Optional[str] = Field(
        default = None,
        serialization_alias = "fromNumber",
        exclude_if = is_none
    )
    to_number: Optional[str] = Field(
        default = None,
        serialization_alias = "toNumber",
        exclude_if = is_none
    )
    mentions: Optional[list[str]] = Field(
        default = None,
        exclude_if = is_none
    )
    user_id: Optional[str] = Field(
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
    email_message_id: Optional[str] = Field(
        default = None,
        validation_alias = "emailMessageId",
    )
    message_ids: Optional[tuple[str]] = Field(
        default = None,
        validation_alias = "messageIds",
    )
    msg: Optional[str] = Field(
        default = None,
    )

    @field_validator("message_ids", mode="before")
    @classmethod
    def validate_message_ids(
        cls,
        value: list[str]
    ) -> tuple[str]:
        return tuple(value)