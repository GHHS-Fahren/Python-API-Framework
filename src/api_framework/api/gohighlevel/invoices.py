from __future__ import annotations

from datetime import datetime

from api_framework.models.gohighlevel.invoices import (
    InvoiceResponse
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class InvoicesAPI:
    _api_client: GHLClient

    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_invoices(
        self,
        *,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        search: str | None = None,
        payment_mode: Literal["default", "live", "test"] | None = None,
        contact_id: str | None = None,
        limit: int | None = 20,
        offset: int | None = 0,
        sort_field: Literal["issueDate"] | None = None,
        sort_order: Literal["ascend", "decend"] | None = None,
        status: Literal[
            "all", "draft", "sent",
            "accepted", "declined",
            "invoiced", "viewed"
        ]|None = None
    ) -> list[InvoiceResponse]:
        invoices = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            "/invoices/",
            params={
                "altId": self._api_client.location_id,
                "altType": "location",
                "status": status,
                "startAt":
                    None if start_at is None
                    else start_at.strftime("%Y-%m-%d"),
                "endAt":
                    None if end_at is None
                    else end_at.strftime("%Y-%m-%d"),
                "search": search,
                "paymentMode": payment_mode,
                "contactId": contact_id,
                "limit": limit,
                "offset": offset,
                "sortField": sort_field,
                "sortOrder": sort_order,
                "status": status
            },
            delete_empty=True
        )["invoices"]
        return [
            InvoiceResponse.model_validate(i)
            for i in invoices
        ]
    
    def get_invoice(
        self,
        invoice_id: str
    ) -> InvoiceResponse:
        invoice = self._api_client.request(
            "GET",
            f"/invoices/{invoice_id}",
            params={
                "altId": self._api_client.location_id,
                "altType": "location"
            }
        )
        return InvoiceResponse.model_validate(invoice)