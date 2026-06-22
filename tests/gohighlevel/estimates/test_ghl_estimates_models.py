from pytest import fixture, raises
from datetime import datetime

from api_framework.models.common.address import FrozenAddress
from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.utils import RemoteFile
from api_framework.models.gohighlevel.estimates import (
    EstimateResponse, EstimateContactResponse,
    EstimateItemsResponse, EstimateItemsTaxResponse,
    EstimateTemplateResponse
)

from typing import Any, override



class TestGHLEstimateItemsTaxResponse(BaseFrozenModelTests):
    model_class = EstimateItemsTaxResponse
    required_field = ("_id", "id")
    optional_field = None
    aliased_field = ("taxId", "tax_id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_estimate_item_tax: dict[str, str|int]
    ):
        self.api_payload = ghl_mock_estimate_item_tax

class TestGHLEstimateItemsResponse(BaseFrozenModelTests):
    model_class = EstimateItemsResponse
    required_field = ("_id", "id")
    optional_field = None
    aliased_field = ("qty", "quantity")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_estimate_item: dict[str, Any]
    ):
        self.api_payload = ghl_mock_estimate_item
    
    def test_for_tax_conversion(self):
        item: EstimateItemsResponse = self.build(self.api_payload)
        assert isinstance(item.taxes, tuple)
        assert isinstance(item.taxes[0], EstimateItemsTaxResponse)
        assert item.taxes[0].name == self.api_payload["taxes"][0]["name"]
    
    def test_for_attachments_conversion(self):
        item: EstimateItemsResponse = self.build(self.api_payload)
        assert isinstance(item.attachments, tuple)
        assert isinstance(item.attachments[0], RemoteFile)
        assert item.attachments[0].name == self.api_payload["attachments"][0]["name"]

class TestGHLEstimateContactResponse(BaseFrozenModelTests):
    model_class = EstimateContactResponse
    required_field = ("id", "id")
    optional_field = None
    aliased_field = ("phoneNo", "phone")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_estimate_contact: dict[str, Any]
    ):
        self.api_payload = ghl_mock_estimate_contact
    
    def test_for_address_conversion(self):
        contact: EstimateContactResponse = self.build(self.api_payload)
        assert isinstance(contact.address, FrozenAddress)
        assert contact.address.state == self.api_payload["address"]["state"]
    
    def test_for_tuple_conversion(self):
        contact: EstimateContactResponse = self.build(self.api_payload)
        # assert isinstance(contact.custom_fields, tuple)
        assert isinstance(contact.additional_emails, tuple)

class TestGHLEstimateResponse(BaseFrozenModelTests):
    model_class = EstimateResponse
    required_field = ("_id", "id")
    optional_field = None
    aliased_field = ("_id", "id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_estimate: dict[str, Any]
    ):
        self.api_payload = ghl_mock_estimate
    
    def test_for_items_conversion(self):
        estimate: EstimateResponse = self.build(self.api_payload)
        assert isinstance(estimate.items, tuple)
        assert isinstance(estimate.items[0], EstimateItemsResponse)
        assert estimate.items[0].id == self.api_payload["items"][0]["_id"]

    def test_for_attachments_conversion(self):
        item: EstimateResponse = self.build(self.api_payload)
        assert isinstance(item.attachments, tuple)
        assert isinstance(item.attachments[0], RemoteFile)
        assert item.attachments[0].name == self.api_payload["attachments"][0]["name"]
    
    def test_for_date_conversion(self):
        item: EstimateResponse = self.build(self.api_payload)
        assert isinstance(item.created_at, datetime)
        assert item.created_at == datetime.fromisoformat(self.api_payload["createdAt"])

class TestGHLEstimateTemplateResponse(TestGHLEstimateResponse):
    model_class = EstimateTemplateResponse

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_estimate_template: dict[str, Any]
    ):
        self.api_payload = ghl_mock_estimate_template