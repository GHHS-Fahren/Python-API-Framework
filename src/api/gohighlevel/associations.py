"""
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
       This code is out of date! Do not use for the time being!       
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
"""

from ...models.gohighlevel.models import AssociationResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api.gohighlevel.api_client import GHLClient

class AssociationsAPI():
    def __init__(
            self,
            api_client: GHLClient
        ) -> None:
        self._api_client = api_client
    
    # @GHLClient.register_scope("associations.readonly")
    def get_associations_by_object_key(
        self,
        object_key: str
    ) -> list[AssociationResponse]:
        associations = self._api_client.request(
            "GET",
            f"/associations/objectKey/{object_key}"
        )
        return [
            AssociationResponse.model_validate(i)
            for i in associations["associations"]
        ]