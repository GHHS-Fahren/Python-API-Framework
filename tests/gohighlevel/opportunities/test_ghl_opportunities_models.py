from pytest import fixture
from datetime import datetime

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.gohighlevel.opportunities \
    import OpportunityResponse

from typing import override, Any



class TestGHLOpportunityResponse(BaseFrozenModelTests):
    model_class = OpportunityResponse
    required_field = ("id", "id")
    optional_field = (None, "assigned_to")
    aliased_field = ("monetaryValue", "value")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_opportunity: dict[str, Any]
    ) -> None:
        self.api_payload = ghl_mock_opportunity
    
    def test_for_datetime_conversion(self):
        opportunity: OpportunityResponse = self.build(self.api_payload)
        assert isinstance(opportunity.created_at, datetime)
        assert opportunity.created_at == datetime.fromisoformat(self.api_payload["createdAt"])
    
    def test_for_tuple_conversion(self):
        opportunity: OpportunityResponse = self.build(self.api_payload)
        assert isinstance(opportunity.followers, tuple)
        assert len(opportunity.followers) == 2