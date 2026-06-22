from __future__ import annotations

from api_framework.models.gohighlevel.opportunities import (
    OpportunityResponse, OpportunityParams
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
        opportunity_data: OpportunityParams
    ) -> OpportunityResponse:
        opportunity = self._api_client.request(
            "POST",
            "/opportunities/upsert",
            json = {
                "id": opportunity_data.get("opportunity_id"),
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
                "lostReasonId": opportunity_data.get("lost_reason_id")
            }
        )["opportunity"]
        return OpportunityResponse.model_validate(opportunity)
    
    def update_opportunity(
        self,
        opportunity_id: str,
        opportunity_data: OpportunityParams
    ) -> OpportunityResponse:
        return self.upsert_opportunity({
            **opportunity_data,
            "opportunity_id": opportunity_id
        })