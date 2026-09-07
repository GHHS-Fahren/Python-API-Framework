from __future__ import annotations

from api_framework.models.gohighlevel.prices import (
    PriceResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class PricesAPI:
    _api_client: GHLClient

    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client

    def search_prices(
        self,
        product_id: str,
        *,
        limit: int = 20,
        offset: int = 0,
        # ids: list[str] | None = None
    ) -> list[PriceResponse]:
        prices = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            f"/products/{product_id}/price",
            params={
                "locationId": self._api_client.location_id,
                "limit": limit,
                "offset": offset,
            }
        )["prices"]
        return [
            PriceResponse.model_validate(i)
            for i in prices
        ]