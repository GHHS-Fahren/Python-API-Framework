from pytest import fixture
from urllib.parse import urljoin

from tests.conftest import SM8_API_ENDPOINT as TEST_ENDPOINT
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import ServiceM8
from api_framework.models.servicem8.company_contacts import CompanyContactResponse

from typing import override



class TestSM8SearchCompanyContacts(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_company_contact_list: list[dict[str, str|int]]
    ) -> None:
        target_url: str = urljoin(
            base = TEST_ENDPOINT,
            url = "companycontact.json?$filter=test%20eq%20%27test%27"
        )
        self.expected_requests = [{"url": target_url}]
        self.request_responses = [{
            "method": "GET",
            "url": target_url,
            "json": sm8_mock_company_contact_list
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", CompanyContactResponse),
            req_field = ("id",sm8_mock_company_contact_list[0]["uuid"])
        )
        self.failure_response = sm8_mock_error
        self.func_reference = sm8_client.company_contacts.search_contacts
        self.func_kwargs = {"filters": "test eq 'test'"}