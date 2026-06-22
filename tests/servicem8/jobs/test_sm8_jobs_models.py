from pytest import fixture
from datetime import datetime

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.servicem8.jobs import JobResponse
from api_framework.models.common.address import FrozenAddress

from typing import override



class TestSM8JobResponse(BaseFrozenModelTests):
    model_class= JobResponse
    required_field = ("uuid", "id")
    optional_field = ("purchase_order_number", "purchase_order_number")
    aliased_field = ("uuid", "id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        sm8_mock_job: dict[str, str|int|float]
    ) -> None:
        self.api_payload = sm8_mock_job

    def test_for_address_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.address, FrozenAddress)
        assert job.address.country == "Australia"

    def test_for_address_optionality(self):
        model_data = {**self.api_payload}
        model_data["geo_is_valid"] = 0
        job: JobResponse = self.build(model_data)
        assert isinstance(job.address, FrozenAddress)
        assert job.address.country is None

    def test_for_datetime_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.created_at, datetime)
        assert job.created_at == datetime(2026,3,1,12)
    
    def test_for_datetime_optionality(self):
        job: JobResponse = self.build(self.api_payload)
        assert job.quote_sent_at is None
    
    def test_for_bool_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.is_address_valid, bool)
        assert job.is_address_valid == True
    
    def test_for_number_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.number, int)
        assert job.number == 558

    def test_for_float_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.invoice_amount, float)
        assert job.invoice_amount == 5.5
    
    def test_for_tuple_conversion(self):
        job: JobResponse = self.build(self.api_payload)
        assert isinstance(job.badges, tuple)
        assert len(job.badges) == 2