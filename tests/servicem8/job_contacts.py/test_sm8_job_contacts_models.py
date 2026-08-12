from pytest import fixture

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.servicem8.job_contacts import (
    JobContactResponse
)

from typing import override



class TestSM8JobMaterialResponse(BaseFrozenModelTests):
    model_class = JobContactResponse
    required_field = ("uuid", "id")
    optional_field = ("phone", "phone")
    aliased_field = ("uuid", "id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_mock_job_contact: dict[str, str|int]
    ) -> None:
        self.api_payload = sm8_mock_job_contact