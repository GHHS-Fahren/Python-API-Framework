from pytest import fixture

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.servicem8.company_contacts \
    import CompanyContactResponse

from typing import override



class TestSM8CompanyContactResponse(BaseFrozenModelTests):
    model_class = CompanyContactResponse
    required_field = ("uuid", "id")
    optional_field = ("email", "email")
    aliased_field = ("uuid", "id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_mock_company_contact: dict[str, str|int]
    ) -> None:
        self.api_payload = sm8_mock_company_contact