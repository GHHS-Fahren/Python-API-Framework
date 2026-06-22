from pytest import fixture

from tests.conftest import SM8_API_ENDPOINT as TEST_ENDPOINT
from tests.common.generic_api_tests import BaseApiEndpointTests, ValuePath
from api_framework import ServiceM8
from api_framework.models.servicem8.job_materials \
    import JobMaterialResponse

from typing import override



JOB_MATERIAL_SEARCH_URL = "jobmaterial.json?$filter=test%20eq%20%27test%27"
JOB_MATERIAL_CREATE_URL = "jobmaterial.json"
JOB_MATERIAL_URL = "jobmaterial/123e4567-74e3-4f64-b22f-23f94bbf232b.json"

class TestSM8SearchJobMaterials(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_material_list: list[dict[str, str|int]]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.expected_requests = [{
            "url": self.build_url(JOB_MATERIAL_SEARCH_URL)
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(JOB_MATERIAL_SEARCH_URL),
            "json": sm8_mock_job_material_list
        }]
        self.success_assertions = self.build_list_generic_asserts(
            obj_inst = ("", JobMaterialResponse),
            req_field = ("id", sm8_mock_job_material_list[0]["uuid"])
        )
        self.failure_response = sm8_mock_error
        self.func_reference = sm8_client.job_materials.search_materials
        self.func_kwargs = {"filters": "test eq 'test'"}

class TestSM8GetJobMaterial(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_material: dict[str, str|int]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_materials.get_job_material
        self.func_kwargs = {
            "job_material_id": sm8_mock_job_material["uuid"]
        }
        self.expected_requests = [{
            "url": self.build_url(JOB_MATERIAL_URL)
        }]
        self.request_responses = [{
            "method": "GET",
            "url": self.build_url(JOB_MATERIAL_URL),
            "json": sm8_mock_job_material
        }]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobMaterialResponse),
            req_field = ("id", sm8_mock_job_material["uuid"])
        )
        self.failure_response = sm8_mock_error

class TestSM8CreateJobMaterial(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_material: dict[str, str|int]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_materials.create_job_material
        self.func_kwargs = {
            "job_material_data": {
                "job_id": sm8_mock_job_material["job_uuid"],
                "material_id": sm8_mock_job_material["material_uuid"],
                "quantity": float(sm8_mock_job_material["quantity"])
            }
        }
        self.expected_requests = [
            {
                "url": self.build_url(JOB_MATERIAL_CREATE_URL),
                "json": {
                    "job_uuid": sm8_mock_job_material["job_uuid"],
                    "material_uuid": sm8_mock_job_material["material_uuid"],
                    "quantity": sm8_mock_job_material["quantity"]
                }
            }, {
                "url": self.build_url(JOB_MATERIAL_URL)
            }
        ]
        self.request_responses = [
            {
                "method": "POST",
                "url": self.build_url(JOB_MATERIAL_CREATE_URL),
                "json": {
                    "errorCode": "0",
                    "message": "OK"
                },
                "headers": {
                    "x-record-uuid": sm8_mock_job_material["uuid"]
                }
            }, {
                "method": "GET",
                "url": self.build_url(JOB_MATERIAL_URL),
                "json": sm8_mock_job_material
            }
        ]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobMaterialResponse),
            req_field = ("id", sm8_mock_job_material["uuid"])
        )
        self.failure_response = sm8_mock_error

class TestSM8UpdateJobMaterial(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_material: dict[str, str|int|float]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_materials.update_job_material
        self.func_kwargs = {
            "job_material_id": sm8_mock_job_material["uuid"],
            "job_material_data": {
                "job_id": sm8_mock_job_material["job_uuid"],
                "material_id": sm8_mock_job_material["material_uuid"],
                "quantity": float(sm8_mock_job_material["quantity"])
            }
        }
        self.expected_requests = [
            {
                "url": self.build_url(JOB_MATERIAL_URL),
                "json": {
                    "job_uuid": sm8_mock_job_material["job_uuid"],
                    "material_uuid": sm8_mock_job_material["material_uuid"],
                    "quantity": sm8_mock_job_material["quantity"]
                }
            }, {
                "url": self.build_url(JOB_MATERIAL_URL)
            }
        ]
        self.request_responses = [
            {
                "method": "POST",
                "url": self.build_url(JOB_MATERIAL_URL),
                "json": {
                    "errorCode": "0",
                    "message": "OK"
                }
            }, {
                "method": "GET",
                "url": self.build_url(JOB_MATERIAL_URL),
                "json": sm8_mock_job_material
            }
        ]
        self.success_assertions = self.build_generic_asserts(
            obj_inst = ("", JobMaterialResponse),
            req_field = ("id", sm8_mock_job_material["uuid"])
        )
        self.failure_response = sm8_mock_error

class TestSM8DeleteJobMaterial(BaseApiEndpointTests):
    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_client: ServiceM8,
        sm8_mock_error: dict[str, str|int],
        sm8_mock_job_material: dict[str, str|int|float]
    ) -> None:
        self.endpoint_base = TEST_ENDPOINT
        self.func_reference = sm8_client.job_materials.delete_job_material
        self.func_kwargs = {
            "job_material_id": sm8_mock_job_material["uuid"],
        }
        self.expected_requests = [{
            "url": self.build_url(JOB_MATERIAL_URL)
        }]
        self.request_responses = [{
            "method": "DELETE",
            "url": self.build_url(JOB_MATERIAL_URL),
            "json": {
                "errorCode": "0",
                "message": "OK"
            }
        }]
        self.success_assertions = [{
            "op": "eq",
            "vals": [ValuePath(""), True]
        }]
        self.failure_response = sm8_mock_error