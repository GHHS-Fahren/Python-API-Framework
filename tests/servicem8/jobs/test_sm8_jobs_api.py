from pytest import fixture
from json import loads

from tests.conftest import SM8_API_ENDPOINT
from tests.common.generic_api_tests import BaseApiEndpointTests
from api_framework import ServiceM8
from api_framework.models.servicem8.jobs import JobResponse

from typing import override



GET_JOB_URL = "job/123e4567-8944-4763-8b13-23f9477acddb.json"
CREATE_FROM_TEMPLATE_URL = "jobtemplate/123e4567-8944-4763-8b13-23f9477acddb/job.json"

class TestSM8GetJob(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job: dict[str, str|int|float]
    ) -> None:
        self.endpoint_base = SM8_API_ENDPOINT
        self.expected_requests = [{
            "url": self.build_url(GET_JOB_URL)
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(GET_JOB_URL),
            "json": sm8_mock_job
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobResponse),
            req_field = ("id", sm8_mock_job["uuid"])
        )
        self.failure_response = sm8_mock_error
        self.func_reference = sm8_client.jobs.get_job
        self.func_kwargs = {
            "job_id": sm8_mock_job["uuid"]
        }

class TestSM8CreateFromTemplate(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job: dict[str, str|int|float]
    ) -> None:
        self.endpoint_base = SM8_API_ENDPOINT
        self.func_reference = sm8_client.jobs.create_from_template
        self.func_kwargs = {
            "template_id": "123e4567-8944-4763-8b13-23f9477acddb",
            "description": "test description",
            "company_id": "123e4567-8944-4763-8b13-23f9477acddb",
            "company_name": "Test company name",
            "address": "8/24-26 Hancock Way,\nBaringa QLD 4551"
        }
        self.expected_requests = [
            {
                "url": self.build_url(CREATE_FROM_TEMPLATE_URL),
                "json": {
                    "job_description": self.func_kwargs["description"],
                    "company_uuid": self.func_kwargs["company_id"],
                    "job_address": self.func_kwargs["address"]
                }
            }, {
                "url": self.build_url(GET_JOB_URL)
            }
        ]
        self.request_responses = [
            {
                "method": "POST",
                "url": self.build_url(CREATE_FROM_TEMPLATE_URL),
                "json": {
                    "jobUUID": sm8_mock_job["uuid"],
                    "location": f"/api_1.0/job/{sm8_mock_job["uuid"]}.json",
                    "message": "Job created successfully"
                }
            }, {
                "method": "GET",
                "url": self.build_url(GET_JOB_URL),
                "json": sm8_mock_job
            }
        ]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobResponse),
            req_field = ("id", sm8_mock_job["uuid"])
        )
        self.failure_response = sm8_mock_error
    
    def test_for_company_name_in_body(self):
        company_name = self.func_kwargs["company_name"]

        expected_json = {
            **self.expected_requests[0]["json"]
        }
        expected_json["company_name"] = company_name
        del expected_json["company_uuid"]

        func_kwargs: dict[str, str] = {**self.func_kwargs}
        del func_kwargs["company_id"]

        _, calls = self._run_func(
            200, self.request_responses, func_kwargs
        )
        assert loads(calls[0].request.body) == expected_json

class TestSM8UpdateJob(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job: dict[str, str|int|float]
    ) -> None:
        self.endpoint_base = SM8_API_ENDPOINT
        self.func_reference = sm8_client.jobs.update_job
        self.func_kwargs = {
            "job_id": sm8_mock_job["uuid"],
            "job_data": {
                "status": sm8_mock_job["status"],
                "description": sm8_mock_job["job_description"]
            }
        }
        self.expected_requests = [
            {
                "url": self.build_url(GET_JOB_URL),
                "json": {
                    "status": sm8_mock_job["status"],
                    "job_description": sm8_mock_job["job_description"],
                }
            }, {
                "url": self.build_url(GET_JOB_URL)
            }
        ]
        self.request_responses = [
            {
                "method": "POST",
                "url": self.build_url(GET_JOB_URL),
                "json": {
                    "errorCode": "0",
                    "message": "OK"
                }
            }, {
                "method": "GET",
                "url": self.build_url(GET_JOB_URL),
                "json": sm8_mock_job
            }
        ]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobResponse),
            req_field = ("id", sm8_mock_job["uuid"])
        )
        self.failure_response = sm8_mock_error