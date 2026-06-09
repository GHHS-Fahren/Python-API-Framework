from __future__ import annotations

from os.path import splitext

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api.gohighlevel.api_client import GHLClient
    from src.models.common.file_models import RemoteFile



class CustomFieldAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self._api_client = api_client

    # @GHLClient.register_scope("locations/customFields.write")
    def upload_to_custom_fields(
        self,
        field_id: str,
        files: dict[str, RemoteFile]
    ) -> dict[str, str]:
        """
        Automatically downloads the remote file and uploads provided
        data to to the custom field and returns the uploaded urls.
        
        Keep in mind if you plan to upload to a custom field with type
        restrictions, its reccommended to include a mime type in the
        remote file object. By default the object will try and guess
        the mime type on the name but without specification,
        GoHighLevel will assume it is a plain text document and may
        not allow you to insert into the custom field.
        """
        urls = self._api_client.request(
            "POST",
            f"/locations/{self._api_client.location_id}/customFields/upload",
            data = {
                "id": field_id,
                "maxFiles": len(files)
            },
            files = {
                k: (
                    f"file_{i}{splitext(file.name)[1]}",
                    file.get_data(),
                    file.mime
                )
                for i,(k,file) in enumerate(files.items())
            }
        )["meta"]
        return {
            file["fieldname"]: file["url"]
            for file in urls
        }