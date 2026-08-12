from pytest import fixture

from tests.conftest import SM8_API_ENDPOINT as TEST_ENDPOINT
from tests.common.generic_api_tests import BaseApiEndpointTests, ValuePath
from api_framework import ServiceM8
from api_framework.models.servicem8.job_contacts import JobContactResponse

from typing import override



JOB_CONTACT_CREATE_URL = "jobcontact.json"
JOB_CONTACT_URL = "jobcontact/123e4567-74e3-4f64-b22f-23f94bbf232b.json"

class TestSM8GetJobContact(BaseApiEndpointTests):
    @fixture(autouse=True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_contact: dict[str, str|int]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_contacts.get_job_contact
        self.func_kwargs = {
            "job_contact_id": sm8_mock_job_contact["uuid"]
        }
        self.expected_requests = [{
            "url": self.build_url(JOB_CONTACT_URL)
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(JOB_CONTACT_URL),
            "json": sm8_mock_job_contact
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobContactResponse),
            req_field = ("id", sm8_mock_job_contact["uuid"])
        )
        self.failure_response = sm8_mock_error

class TestSM8CreateJobContact(BaseApiEndpointTests):
    @fixture(autouse=True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_contact: dict[str, str|int]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_contacts.create_job_contact
        self.func_kwargs = {
            "job_contact_data": {
                "job_id": sm8_mock_job_contact["job_uuid"],
                "type": sm8_mock_job_contact["type"],
                "first": sm8_mock_job_contact["first"],
                "last": sm8_mock_job_contact["last"],
                "phone": sm8_mock_job_contact["phone"],
                "mobile": sm8_mock_job_contact["mobile"],
                "email": sm8_mock_job_contact["email"],
            }
        }
        self.expected_requests = [
            {
                "url": self.build_url(JOB_CONTACT_CREATE_URL),
                "json": {
                    "job_uuid": sm8_mock_job_contact["job_uuid"],
                    "type": sm8_mock_job_contact["type"],
                    "first": sm8_mock_job_contact["first"],
                    "last": sm8_mock_job_contact["last"],
                    "phone": sm8_mock_job_contact["phone"],
                    "mobile": sm8_mock_job_contact["mobile"],
                    "email": sm8_mock_job_contact["email"],
                }
            }, {
                "url": self.build_url(JOB_CONTACT_URL)
            }
        ]
        self.request_responses = [
            {
                "method": "POST",
                "url": self.build_url(JOB_CONTACT_CREATE_URL),
                "json": {
                    "errorCode": "0",
                    "message": "OK"
                },
                "headers": {
                    "x-record-uuid": sm8_mock_job_contact["uuid"]
                }
            }, {
                "method": "GET",
                "url": self.build_url(JOB_CONTACT_URL),
                "json": sm8_mock_job_contact
            }
        ]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobContactResponse),
            req_field = ("id", sm8_mock_job_contact["uuid"])
        )
        self.failure_response = sm8_mock_error