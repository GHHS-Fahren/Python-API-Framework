from pytest import fixture
from datetime import datetime, timedelta
from urllib.parse import quote

from tests.conftest import GHL_API_ENDPOINT, GHL_API_LOCATION
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import GoHighLevel
from api_framework.models.gohighlevel.estimates import (
    EstimateResponse,
    EstimateTemplateResponse
)

from typing import override



# Note this test does both the get_estimate and search_estimates
# as the get estimates is a wrapper for the search estimate
class TestGHLSearchEstimates(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_estimate_list_ret: dict[str, Any]
    ) -> None:
        start_at = datetime.now() - timedelta(days=7)
        end_at = datetime.now()
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.estimates.search_estimates
        self.func_kwargs = {
            "limit": 5,
            "offset": 1,
            "start_at": start_at,
            "end_at": end_at,
            "search": "test search",
            "contact_id": "6a2794b8dc7eb330de33361a",
            "status": "all"
        }
        self.expected_requests = [{
            "url": self.build_url("invoices/estimate/list"),
            "params": {
                "altId": GHL_API_LOCATION,
                "altType": "location",
                "startAt": start_at.strftime("%Y-%m-%d"),
                "endAt": end_at.strftime("%Y-%m-%d"),
                "search": quote(self.func_kwargs["search"]),
                "contactId": self.func_kwargs["contact_id"],
                "status": "all",
                "limit": self.func_kwargs["limit"],
                "offset": self.func_kwargs["offset"]
            }
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url("invoices/estimate/list"),
            "json": ghl_mock_estimate_list_ret,
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", EstimateResponse),
            req_field = (
                "id",
                ghl_mock_estimate_list_ret["estimates"][0]["_id"]
            )
        )
        self.failure_response = ghl_mock_error

class TestGHLGetEstimate(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_estimate_list_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.estimates.get_estimate
        self.func_kwargs = {
            "estimate_id": "6a2794b8dc7eb330de33361a"
        }
        self.expected_requests = [{
            "url": self.build_url("invoices/estimate/list"),
            "params": {
                "altId": GHL_API_LOCATION,
                "altType": "location",
                "search": quote(self.func_kwargs["estimate_id"]),
                "limit": 1,
                "offset": 0
            }
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url("invoices/estimate/list"),
            "json": ghl_mock_estimate_list_ret,
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", EstimateResponse),
            req_field = (
                "id",
                ghl_mock_estimate_list_ret["estimates"][0]["_id"]
            )
        )
        self.failure_response = ghl_mock_error

# Note this test does both the get_template and search_templates
# as the get templates is a wrapper for the search estimate
class TestGHLSearchTemplates(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_estimate_template_list_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.estimates.search_templates
        self.func_kwargs = {
            "limit": 5,
            "offset": 1,
            "search": "test search"
        }
        self.expected_requests = [{
            "url": self.build_url("invoices/estimate/template"),
            "params": {
                "altId": GHL_API_LOCATION,
                "altType": "location",
                "search": quote(self.func_kwargs["search"]),
                "limit": self.func_kwargs["limit"],
                "offset": self.func_kwargs["offset"]
            }
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url("invoices/estimate/template"),
            "json": ghl_mock_estimate_template_list_ret,
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", EstimateTemplateResponse),
            req_field = (
                "id",
                ghl_mock_estimate_template_list_ret["data"][0]["_id"]
            )
        )
        self.failure_response = ghl_mock_error

class TestGHLGetTemplate(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_estimate_template_list_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.estimates.get_template
        self.func_kwargs = {
            "template_id": "6a2794b8dc7eb330de33361a"
        }
        self.expected_requests = [{
            "url": self.build_url("invoices/estimate/template"),
            "params": {
                "altId": GHL_API_LOCATION,
                "altType": "location",
                "search": quote(self.func_kwargs["template_id"]),
                "limit": 1,
                "offset": 0
            }
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url("invoices/estimate/template"),
            "json": ghl_mock_estimate_template_list_ret,
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", EstimateTemplateResponse),
            req_field = (
                "id",
                ghl_mock_estimate_template_list_ret["data"][0]["_id"]
            )
        )
        self.failure_response = ghl_mock_error