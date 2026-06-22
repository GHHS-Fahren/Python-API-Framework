from __future__ import annotations

from urllib.parse import quote

from api_framework.models.servicem8.company_contacts import (
    CompanyContactResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client



class CompanyContactAPI():
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client
    
    def search_contacts(
        self,
        filters: str|None = None
    ) -> list[CompanyContactResponse]:
        url = "companycontact.json"
        if filters: url += f"?$filter={quote(filters)}"
        contacts = self._api_client.request(
            "GET",
            url
        )
        return [
            CompanyContactResponse.model_validate(i)
            for i in contacts
        ]