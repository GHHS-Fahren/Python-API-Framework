from pytest import fixture

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.servicem8.job_materials \
    import JobMaterialResponse

from typing import override



class TestSM8JobMaterialResponse(BaseFrozenModelTests):
    model_class = JobMaterialResponse
    required_field = ("uuid", "id")
    optional_field = ("name", "name")
    aliased_field = ("uuid", "id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_mock_job_material: dict[str, str|int]
    ) -> None:
        self.api_payload = sm8_mock_job_material