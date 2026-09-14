from __future__ import annotations

from api_framework.models.gohighlevel.opportunities import (
    OpportunityResponse, OpportunityParams, OpportunityCreate
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



class OpportunitiesAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    def get_opportunity(
        self,
        opportunity_id: str
    ) -> OpportunityResponse:
        opportunity = self._api_client.request(
            "GET",
            f"/opportunities/{opportunity_id}",
        )["opportunity"]
        return OpportunityResponse.model_validate(opportunity)
    
    def upsert_opportunity(
        self,
        opportunity_id: str|None,
        opportunity_data: OpportunityParams
    ) -> OpportunityResponse:
        opportunity = self._api_client.request(
            "POST",
            "/opportunities/upsert",
            json = {
                "id": opportunity_id,
                "contactId": opportunity_data["contact_id"],
                "pipelineId": opportunity_data.get("pipeline_id"),
                "locationId": self._api_client.location_id,
                "followers": opportunity_data.get("followers"),
                "isRemoveAllFollowers":
                    opportunity_data.get("is_remove_all_followers"),
                "followersActionType":
                    opportunity_data.get("followers_action_type"),
                "name": opportunity_data.get("name"),
                "status": opportunity_data.get("status"),
                "pipelineStageId": opportunity_data.get("pipeline_stage_id"),
                "monetaryValue": opportunity_data.get("value"),
                "forecastExpectedCloseDate":
                    opportunity_data.get("forecast_expected_close_date"),
                "assignedTo": opportunity_data.get("assigned_to"),
                "lostReasonId": opportunity_data.get("lost_reason_id"),
                "customFields": opportunity_data.get("custom_fields")
            }
        )["opportunity"]
        return OpportunityResponse.model_validate(opportunity)
    
    def update_opportunity(
        self,
        opportunity_id: str,
        contact_id: str,
        opportunity_data: OpportunityParams
    ) -> OpportunityResponse:
        return self.upsert_opportunity(
            opportunity_id = opportunity_id,
            opportunity_data = {
                **opportunity_data,
                "opportunity_id": opportunity_id,
                "contact_id": contact_id
            }
        )
    
    def create_opportunity(
        self,
        opportunity_data: OpportunityCreate
    ) -> OpportunityResponse:
        opportunity = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "POST",
            "/opportunities",
            json={
                "locationId": self._api_client.location_id,
                "pipelineId": opportunity_data["pipeline_id"],
                "contactId": opportunity_data["contact_id"],
                "name": opportunity_data["name"],
                "status": opportunity_data["status"],
                "pipelineStageId":
                    opportunity_data.get("pipeline_stage_id"),
                "monetaryValue": opportunity_data.get("value"),
                "forecastExpectedCloseDate":
                    opportunity_data.get("forecast_expected_close_date"),
                "forecastProbability":
                    opportunity_data.get("forecast_probability"),
                "assignedTo": opportunity_data.get("assigned_to"),
                "customFields": opportunity_data.get("custom_fields")
            },
            delete_empty=True
        )["opportunity"]
        return OpportunityResponse.model_validate(opportunity)
    
    def search_opportunities(
        self,
        *,
        query: str | None = None,
        page: int = 1,
        limit: int = 20,
        pipeline_id: str | None = None,
        pipeline_stage_id: str | None = None,
    ) -> list[OpportunityResponse]:
        opportunities = self._api_client.request(  # pyright: ignore[reportCallIssue, reportArgumentType]
            "GET",
            "/opportunities/search",
            params={
                "location_id": self._api_client.location_id,
                "q": query,
                "page": page,
                "limit": limit,
                "pipelineId": pipeline_id,
                "pipelineStageId": pipeline_stage_id
            },
            delete_empty=True
        )["opportunities"]
        return [
            OpportunityResponse.model_validate(i)
            for i in opportunities
        ]