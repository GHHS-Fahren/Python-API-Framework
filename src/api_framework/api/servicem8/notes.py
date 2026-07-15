from __future__ import annotations

from api_framework.models.servicem8.notes import NoteResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client



class NotesAPI():
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client
    
    def get_note(
        self,
        note_id: str
    ) -> NoteResponse:
        note = self._api_client.request(
            "GET",
            f"dbonote/{note_id}.json"
        )
        return NoteResponse.model_validate(note)

    def create_note(
        self,
        related_object: str,
        related_object_id: str,
        note: str
    ) -> NoteResponse:
        _, headers = self._api_client.request(
            "POST",
            "note.json",
            return_headers = True,
            json = {
                "related_object": related_object,
                "related_object_uuid": related_object_id,
                "note": note
            }
        )
        return self.get_note(headers["x-record-uuid"])