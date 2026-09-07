from __future__ import annotations

from api_framework.models.gohighlevel.products import (
    ProductResponse
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class ProductsAPI:
    _api_client: GHLClient

    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_products(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        # collections: list[str] | None = None,
        collection_slug: str | None = None,
        # expand: list[str] | None = None,
        # product_ids: list[str] | None = None,
        # store_id: str | None = None,
        # is_included_in_store: bool | None = None,
        # is_available_in_store: bool | None = None,
        sort_order: Literal["ascend", "decend"] | None = None
    ) -> list[ProductResponse]:
        products = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            "/products/",
            params={
                "locationId": self._api_client.location_id,
                "limit": limit,
                "offset": offset,
                "search": search,
                "collectionSlug": collection_slug,
                "sortOrder": sort_order
            },
            delete_empty=True
        )["products"]
        return [
            ProductResponse.model_validate(i)
            for i in products
        ]