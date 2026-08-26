from __future__ import annotations

from datetime import datetime

from api_framework.models.gohighlevel.transactions import (
    TransactionResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class TransactionsAPI:
    _api_client: GHLClient

    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_transactions(
        self,
        *,
        payment_mode: str | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
        entity_source_type: str | None = None,
        entity_source_sub_type: str | None = None,
        search: str | None = None,
        subscription_id: str | None = None,
        entity_id: str | None = None,
        contact_id: str | None = None,
        limit: int | None = 20,
        offset: int | None = 0
    ) -> list[TransactionResponse]:
        transactions = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            "/payments/transactions",
            params={
                "altId": self._api_client.location_id,
                "altType": "location",
                "paymentMode": payment_mode,
                "startAt":
                    None if start_at is None
                    else start_at.strftime("%Y-%m-%d"),
                "endAt":
                    None if end_at is None
                    else end_at.strftime("%Y-%m-%d"),
                "entitySourceType": entity_source_type,
                "entitySourceSubType": entity_source_sub_type,
                "search": search,
                "subscriptionId": subscription_id,
                "entityId": entity_id,
                "contactId": contact_id,
                "limit": limit,
                "offset": offset
            },
            delete_empty=True
        )["data"]
        return [
            TransactionResponse.model_validate(i)
            for i in transactions
        ]

    def get_transaction(
        self,
        transaction_id: str
    ) -> TransactionResponse:
        transaction = self._api_client.request(
            "GET",
            f"/invoices/{transaction_id}",
            params={
                "altId": self._api_client.location_id,
                "altType": "location"
            }
        )
        return TransactionResponse.model_validate(transaction)