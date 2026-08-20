from __future__ import annotations

from api_framework.models.gohighlevel.contacts import (
    ContactNoteResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class ContactsAPI:
    _api_client: GHLClient

    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_notes(
        self,
        *,
        contact_id: str
    ) -> list[ContactNoteResponse]:
        notes = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            f"/contacts/{contact_id}/notes"
        )["notes"]
        return [
            ContactNoteResponse.model_validate(i)
            for i in notes
        ]