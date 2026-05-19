from __future__ import annotations

from .models import CustomObjectRequest, CustomObjectResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.ghl.client import GHLClient
    from collections.abc import Iterator



class CustomObjectRecordAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client
    
    # @GHLClient.register_scope("objects/record.readonly")
    def get_record(
        self,
        object_key: str,
        record_id: str
    ) -> CustomObjectResponse:
        """
        Retrieves the given record data from GoHighLevel
        """
        record = self._api_client.request(
            "GET",
            f"/objects/{object_key}/records/{record_id}",
            params = {"locationId": self._api_client.location_id}
        )["record"]
        return CustomObjectResponse.model_validate(record)
    
    # @GHLClient.register_scope("objects/record.readonly")
    def search_records(
        self,
        object_key: str,
        page: int = 1,
        limit: int = 20,
        query: str|None = None,
        filters: list[dict]|None = None,
        search_after: list[str]|None = None
    ) -> list[CustomObjectResponse]:
        """
        Searches the custom object records that match the given
        filters. Returns a list of custom object responses.
        """
        json = {
            "locationId": self._api_client.location_id,
            "page": page,
            "pageLimit": limit,
        }
        if query: json["q"] = query
        if filters: json["filters"] = filters
        if search_after: json["searchAfter"] = search_after
        records = self._api_client.request(
            "POST",
            f"/objects/{object_key}/records/search",
            json = json
        )["records"]
        return [
            CustomObjectResponse.model_validate(i)
            for i in records
        ]
    
    # @GHLClient.register_scope("objects/record.readonly")
    def iter_search_records(
        self,
        object_key: str,
        query: str|None = None,
        filters: list[dict]|None = None,
        search_after: list[str]|None = None
    ) -> Iterator[CustomObjectResponse]:
        """
        Searches the custom object records that match the given
        filters. Returns an iterator of a list of custom object
        responses.
        """
        page = 1
        while True:
            records = self.search_records(
                object_key,
                page = page,
                limit = 20,
                query = query,
                filters = filters,
                search_after = search_after
            )
            if not records: break
            yield from [
                CustomObjectResponse.model_validate(i)
                for i in records
            ]
            page += 1
    
    # @GHLClient.register_scope("objects/record.write")
    def create_record(
        self,
        object_key: str,
        record_data: CustomObjectRequest
    ) -> CustomObjectResponse:
        """
        Creates a new custom object record in GoHighLevel with the
        data provided in the custom object request
        """
        record = self._api_client.request(
            "POST",
            f"/objects/{object_key}/records",
            json = {
                **record_data.model_dump(),
                "locationId": self._api_client.location_id
            }
        )["record"]
        return CustomObjectResponse.model_validate(record)
    
    # @GHLClient.register_scope("objects/record.write")
    def update_record(
        self,
        object_key: str,
        record_id: str,
        record_data: CustomObjectRequest
    ) -> CustomObjectResponse:
        """
        Updates a custom object with the provided data.
        """
        record = self._api_client.request(
            "PUT",
            f"/objects/{object_key}/records/{record_id}",
            params = {"locationId": self._api_client.location_id},
            json = record_data.model_dump()
        )["record"]
        return CustomObjectResponse.model_validate(record)