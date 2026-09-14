from __future__ import annotations

from api_framework.models.gohighlevel.contacts import (
    ContactNoteResponse, ContactResponse, ContactCreate
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

    def create_note(
        self,
        contact_id: str,
        body: str
    ) -> ContactNoteResponse:
        note = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "POST",
            f"/contacts/{contact_id}/notes",
            json={
                "body": body
            }
        )["note"]
        return ContactNoteResponse.model_validate(note)
    
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
        if (email is not None) and (phone is not None):
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
    
    def create_contact(
        self,
        contact_data: ContactCreate
    ) -> ContactResponse:
        contact = self._api_client.request(  # pyright: ignore[reportArgumentType, reportCallIssue]
            "POST",
            "/contact",
            json={
                "locationId": self._api_client.location_id,
                "firstName": contact_data.get("first_name"),
                "lastName": contact_data.get("last_name"),
                "name": contact_data.get("name"),
                "email": contact_data.get("email"),
                "timezone": contact_data.get("timezone"),
                "companyName": contact_data.get("company_name"),
                "phone": contact_data.get("phone"),
                "dnd": contact_data.get("is_dnd"),
                "source": contact_data.get("source"),
                "address1": contact_data.get("address1"),
                "city": contact_data.get("city"),
                "state": contact_data.get("state"),
                "country": contact_data.get("country"),
                "postalCode": contact_data.get("post_code"),
                "website": contact_data.get("website"),
                "tags": contact_data.get("tags"),
                "dateOfBirth":
                    None if "date_of_birth" not in contact_data
                    else contact_data["date_of_birth"].isoformat(),
                "customFields": contact_data.get("custom_fields"),
                "inboundDndSettings": contact_data.get("inbound_dnd_settings"),
                "dndSettings": contact_data.get("dnd_config"),
            },
            delete_empty=True
        )["contact"]
        return ContactResponse.model_validate(contact)