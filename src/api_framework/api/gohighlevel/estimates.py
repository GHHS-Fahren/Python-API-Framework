from __future__ import annotations

from datetime import datetime

from api_framework.models.gohighlevel.estimates import (
    EstimateResponse, EstimateTemplateResponse
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient
    from collections.abc import Iterator



class EstimatesAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def search_estimates(
        self,
        *,
        limit: int|None = 20,
        offset: int|None = 0,
        start_at: datetime|None = None,
        end_at: datetime|None = None,
        search: str|None = None,
        contact_id: str|None = None,
        status: Literal[
            "all", "draft", "sent",
            "accepted", "declined",
            "invoiced", "viewed"
        ]|None = None
    ) -> list[EstimateResponse]:
        estimates = self._api_client.request(  # pyright: ignore[reportArgumentType, reportCallIssue]
            "GET",
            "/invoices/estimate/list",
            params = {
                "altId": self._api_client.location_id,
                "altType": "location",
                "startAt":
                    None if start_at is None
                    else start_at.strftime("%Y-%m-%d"),
                "endAt":
                    None if end_at is None
                    else end_at.strftime("%Y-%m-%d"),
                "search": search,
                "status": status,
                "contactId": contact_id,
                "limit": limit,
                "offset": offset
            },
            delete_empty=True
        )["estimates"]
        return [
            EstimateResponse.model_validate(i)
            for i in estimates
        ]
    
    def get_estimate(
        self,
        estimate_id: str
    ) -> EstimateResponse:
        return self.search_estimates(
            limit = 1,
            search = estimate_id
        )[0]
    
    def search_templates(
        self,
        search: str|None = "",
        limit: int|None = 20,
        offset: int|None = 0
    ) -> list[EstimateTemplateResponse]:
        templates = self._api_client.request(  # pyright: ignore[reportArgumentType, reportCallIssue]
            "GET",
            "/invoices/estimate/template",
            params = {
                "altId": self._api_client.location_id,
                "altType": "location",
                "search": search,
                "limit": limit,
                "offset": offset
            }
        )["data"]
        return [
            EstimateTemplateResponse.model_validate(i)
            for i in templates
        ]
    
    def get_template(
        self,
        template_id: str
    ) -> EstimateTemplateResponse:
        return self.search_templates(
            limit = 1,
            search = template_id
        )[0]