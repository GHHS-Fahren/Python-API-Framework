from __future__ import annotations

from api_framework.models.gohighlevel.contacts import (
    ContactNoteResponse, ContactResponse
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
    
    def get_contact(
        self,
        contact_id: str
    ) -> ContactResponse:
        contact = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            f"/contacts/{contact_id}"
        )["contact"]
        return ContactResponse.model_validate(contact)
    
    def search_contacts(
        self,
        page: int = 0,
        limit: int = 20,
        # filters
        # sort
    ) -> list[ContactResponse]:
        contacts = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "POST",
            "/contacts/search",
            json={
                "locationId": self._api_client.location_id,
                "page": page,
                "pageLimit": limit,
            }
        )["contacts"]
        return [
            ContactResponse.model_validate(i)
            for i in contacts
        ]
    
    def lookup_contact(
        self,
        *,
        email: str | None = None,
        phone: str | None = None,
        next_cursor: str | None = None,
        limit: int = 20
    ) -> list[ContactResponse]:
        if email and phone:
            raise ValueError("email and phone are mutually exclusive")
        contacts = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            "/contacts/lookup",
            params={
                "locationId": self._api_client.location_id,
                "email": email,
                "phone": phone,
                "nextCursor": next_cursor,
                "limit": limit
            },
            delete_empty=True
        )["contacts"]
        return [
            ContactResponse.model_validate(i)
            for i in contacts
        ]
    
    # def create_contact()