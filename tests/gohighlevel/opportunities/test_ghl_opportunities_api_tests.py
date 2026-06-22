from pytest import fixture

from tests.conftest import GHL_API_ENDPOINT, GHL_API_LOCATION
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import GoHighLevel
from api_framework.models.gohighlevel.opportunities \
    import OpportunityResponse#, OpportunityContactResponse

from typing import override, Any



GET_OPPORTUNITY_URL = "opportunities/1234abcd5678efgh9012ijkl"

class TestGHLGetOpportunity(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_opportunity_single_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.opportunities.get_opportunity
        self.func_kwargs = {
            "opportunity_id": "1234abcd5678efgh9012ijkl"
        }
        self.expected_requests = [{
            "url": self.build_url(GET_OPPORTUNITY_URL)
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(GET_OPPORTUNITY_URL),
            "json": ghl_mock_opportunity_single_ret
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", OpportunityResponse),
            req_field = ("id", self.func_kwargs["opportunity_id"])
        )
        self.failure_response = ghl_mock_error

# class TestGHLUpsertOpportunity(BaseApiEndpointTests):
#     @fixture(autouse = True)
#     @override
#     def setup(
#         self,
#         ghl_client: GoHighLevel,
#         ghl_mock_error: dict[str, str|int],
#         ghl_mock_opportunity_single_ret: dict[str, Any]
#     ) -> None:
#         self.endpoint_base = GHL_API_ENDPOINT
#         self.func_reference = ghl_client.opportunities.upsert_opportunity
#         self.func_kwargs - {
#             "opportunity_data": {
#                 "opportunity_id": 
#             }
#         }

class TestGHLUpdateOpportunity(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_opportunity_single_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.opportunities.update_opportunity
        self.func_kwargs = {
            "opportunity_id": "1234abcd5678efgh9012ijkl",
            "opportunity_data": {
                "pipeline_id": "1234abcd5678efgh9012ijkl",
                "pipeline_stage_id": "1234abcd5678efgh9012ijkl"
            }
        }
        self.expected_requests = [{
            "url": self.build_url("/opportunities/upsert"),
            "json": {
                "locationId": GHL_API_LOCATION,
                "id": self.func_kwargs["opportunity_id"],
                "pipelineId": self.func_kwargs["opportunity_data"]["pipeline_id"],
                "pipelineStageId": self.func_kwargs["opportunity_data"]["pipeline_stage_id"]
            }
        }]
        self.request_responses = [{
            "method": "POST",
            "url": self.build_url("/opportunities/upsert"),
            "json": ghl_mock_opportunity_single_ret
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", OpportunityResponse),
            req_field = ("id", self.func_kwargs["opportunity_id"])
        )
        self.failure_response = ghl_mock_error