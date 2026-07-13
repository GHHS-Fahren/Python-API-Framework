from pytest import fixture

from tests.conftest import GHL_API_ENDPOINT, GHL_API_LOCATION
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import GoHighLevel
from api_framework.models.gohighlevel.relations \
    import RelationResponse

from typing import override, Any



class TestGHLGetRelations(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_relation_list_ret: dict[str, Any]
    ) -> None:
        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.relations.get_relations
        self.func_kwargs = {
            "record_id": ghl_mock_relation_list_ret["relations"][0]["firstRecordId"],
            "skip": 5,
            "limit": 30,
            "association_ids": [ghl_mock_relation_list_ret["relations"][0]["associationId"] for _ in range(2)]
        }
        self.expected_requests = [{
            "url": self.build_url(f"/associations/relations/{self.func_kwargs["record_id"]}"),
            "params": {
                "locationId": GHL_API_LOCATION,
                "skip": self.func_kwargs["skip"],
                "limit": self.func_kwargs["limit"],
                "associationIds": ",".join(self.func_kwargs["association_ids"])
            }
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(f"/associations/relations/{self.func_kwargs["record_id"]}"),
            "json": ghl_mock_relation_list_ret
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", RelationResponse),
            req_field = ("id", ghl_mock_relation_list_ret["relations"][0]["id"])
        )
        self.failure_response = ghl_mock_error