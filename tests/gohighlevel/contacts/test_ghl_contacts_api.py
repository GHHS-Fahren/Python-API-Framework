from pytest import fixture
from datetime import datetime, timedelta
from urllib.parse import quote

from tests.conftest import GHL_API_ENDPOINT, GHL_API_LOCATION
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import GoHighLevel
from api_framework.models.gohighlevel.contacts import (
    ContactNoteResponse
)

from typing import override



class TestGHLSearchContactNotes(BaseApiEndpointTests):
    @fixture(autouse=True)
    @override
    def setup(
        self,
        ghl_client: GoHighLevel,
        ghl_mock_error: dict[str, str|int],
        ghl_mock_contact_note_list_ret: dict[str, str|list[dict[str, str|bool|list[dict[str,str]]]]]
    ) -> None:
        contact_id: str = ghl_mock_contact_note_list_ret["notes"][0]["contactId"]  # pyright: ignore[reportArgumentType, reportAssignmentType]

        self.endpoint_base = GHL_API_ENDPOINT
        self.func_reference = ghl_client.contacts.search_notes
        self.func_kwargs = {
            "contact_id": contact_id
        }
        self.expected_requests = [{
            "url": self.build_url(f"/contacts/{contact_id}/notes")
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(f"/contacts/{contact_id}/notes"),
            "json": ghl_mock_contact_note_list_ret
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst=("", ContactNoteResponse),
            req_field=("id", ghl_mock_contact_note_list_ret["notes"][0]["id"])  # pyright: ignore[reportArgumentType]
        )
        self.failure_response = ghl_mock_error