from __future__ import annotations

from .models import RelationResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.ghl.client import GHLClient



class RelationsAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    # @GHLClient.register_scope("associations/relation.write")
    def create_relation(
        self,
        association_id: str,
        first_record_id: str,
        second_record_id: str
    ) -> RelationResponse:
        """
        Creates a new relation between the two records provided.
        """
        relation = self._api_client.request(
            "POST",
            "/associations/relations",
            json = {
                "locationId": self._api_client.location_id,
                "associationId": association_id,
                "firstRecordId": first_record_id,
                "secondRecordId": second_record_id
            }
        )
        return RelationResponse.model_validate(relation)