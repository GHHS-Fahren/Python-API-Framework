from pytest import fixture
from datetime import datetime

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.gohighlevel.contacts import (
    ContactNoteResponse
)

from typing import Any, override



class TestGHLContactNoteResponse(BaseFrozenModelTests):
    model_class = ContactNoteResponse
    required_field = "id", "id"
    optional_field = None
    aliased_field = "contactId", "contact_id"

    @fixture(autouse=True)
    @override
    def setup(
        self,
        ghl_mock_contact_note: dict[str, Any]
    ):
        self.api_payload = ghl_mock_contact_note