from pytest import fixture

from tests.common.generic_model_tests import BaseFrozenModelTests
from api_framework.models.gohighlevel.relations \
    import RelationResponse

from typing import override, Any



class TestGHLRelationResponse(BaseFrozenModelTests):
    model_class = RelationResponse
    required_field = ("id", "id")
    optional_field = None
    aliased_field = ("associationId", "association_id")

    @fixture(autouse = True)
    @override
    def setup(
        self,
        ghl_mock_relation: dict[str, Any]
    ) -> None:
        self.api_payload = ghl_mock_relation

    def test_for_object_conversion(self):
        relation: RelationResponse = self.build(self.api_payload)
        assert isinstance(relation.first_object, RelationResponse._CustomObjectData)
        assert relation.first_object.key == self.api_payload["firstObjectKey"]