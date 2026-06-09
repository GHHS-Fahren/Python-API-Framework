from __future__ import annotations

from api_framework.models.gohighlevel.messages import (
    CreateEmailParams, CreateMessageRequest, CreateMessageResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class MessagesAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def _create_message(
        self,
        message_data: CreateMessageRequest
    ) -> CreateMessageResponse:
        message = self._api_client.request(
            "POST",
            "/conversations/messages",
            json = {
                **message_data.model_dump()
            }
        )
        return CreateMessageResponse.model_validate(message)
    
    def send_email(
        self,
        contact_id: str,
        email_params: CreateEmailParams
    ) -> CreateMessageResponse:
        message_data = CreateMessageRequest.model_validate({
            "type": "Email",
            "status": "pending",
            "contact_id": contact_id,
            "appointment_id": email_params["appointment_id"],
            "email_from": email_params["email_from"],
            "email_to": email_params["email_to"],
            "email_cc": email_params["email_cc"],
            "email_bcc": email_params["email_bcc"],
            "subject": email_params["subject"],
            "html": email_params["html"],
            "email_reply_mode": email_params["email_reply_mode"],
            "reply_message_id": email_params["reply_message_id"],
            "template_id": email_params["template_id"],
            "thread_id": email_params["thread_id"],
            "scheduled_timestamp": email_params["scheduled_timestamp"]
        })
        return self._create_message(message_data)