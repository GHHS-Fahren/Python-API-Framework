from pytest import fixture

from tests.conftest import GHL_API_ENDPOINT, GHL_API_LOCATION
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import GoHighLevel
from api_framework.models.gohighlevel.objects \
    import CustomObjectResponse

from typing import override, Any



SEARCH_ENDPOINT = "objects/custom_objects.example"

class TestGHLSearchRecords(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_record_list_ret: dict[str, Any]
    ) -> None:
        ENDPOINT = f"objects/{ghl_mock_record_list_ret["records"][0]["objectKey"]}/records/search"
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.records.search_records
        self.func_kwargs = {
            "object_key": ghl_mock_record_list_ret["records"][0]["objectKey"],
            "page": 2,
            "limit": 15,
            "query": "test search",
            "filters": [{
                "field": "properties.example",
                "operator": "eq",
                "value": "test"
            }],
            "search_after": [
                1738683828372,
                "67a235b49b289431bcf657f8"
            ]
        }
        self.expected_requests = [{
            "url": self.build_url(ENDPOINT),
            "json": {
                "locationId": GHL_API_LOCATION,
                "page": self.func_kwargs["page"],
                "pageLimit": self.func_kwargs["limit"],
                "query": self.func_kwargs["query"],
                "filters": [{**self.func_kwargs["filters"][0]}],
                "searchAfter": [*self.func_kwargs["search_after"]]
            }
        }]
        self.request_responses = [{
            "method": "POST",
            "url": self.build_url(ENDPOINT),
            "json": ghl_mock_record_list_ret
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", CustomObjectResponse),
            req_field = ("object_key", self.func_kwargs["object_key"])
        )
        self.failure_response = ghl_mock_error