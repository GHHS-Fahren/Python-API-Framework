from __future__ import annotations

from urllib.parse import urlencode, quote

from api_framework.models.gohighlevel.relations import RelationResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.gohighlevel.api_client import GHLClient



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
    
    def get_relations(
        self,
        record_id: str,
        skip: int = 0,
        limit: int = 20,
        association_ids: list[str]|None = None
    ) -> list[RelationResponse]:
        encoded_params = urlencode(
            query = {
                "locationId": self._api_client.location_id,
                "skip": skip,
                "limit": limit,
            },
            quote_via = quote
        )
        if association_ids:
            new_ids = [
                quote(string=i)
                for i in association_ids
            ]
            encoded_params += f"&associationIds={','.join(new_ids)}"
        relations = self._api_client.request(
            "GET",
            f"associations/relations/{record_id}?{encoded_params}"
        )["relations"]
        return [
            RelationResponse.model_validate(i)
            for i in relations
        ]