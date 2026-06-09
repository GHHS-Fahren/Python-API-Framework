from __future__ import annotations

from src.models.gohighlevel.forms import FormSubmissionResponse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import datetime
    from src.api.gohighlevel.api_client import GHLClient
    from collections.abc import Iterator

class FormAPI():
    def __init__(
        self,
        api_client: GHLClient
    ) -> None:
        self.api_client = api_client

    # @GHLClient.register_scope("forms.readonly")
    def get_form_submissions(
        self,
        form_id: str|None = None,
        name_mappings: dict[str, str]|None = None,
        page: int = 1,
        limit: int = 20,
        query: str|None = None,
        start_at: datetime|None = None,
        end_at: datetime|None = None
    ) -> list[FormSubmissionResponse]:
        """
        Retrieves form submissions that match the criteria and returns
        them in a list of `FormSubmissionResponse`. Params are as the
        GHL API docs describe as. When `name_mappings` is passed, all
        returned form objects can reference their fields by the
        mapping. Note: ALL form objects will receive the same mapping,
        if multiple different forms are returned, leave blank and
        manually call `form.fields.set_name_map(mappings)`.
        """
        responses = self.api_client.request(
            "GET",
            "/forms/submissions",
            params = {
                "locationId": self.api_client.location_id,
                "page": page,
                "limit": limit,
                "formId": form_id,
                "q": query,
                "startAt": start_at.strftime("%Y/%m/%d")
                    if start_at else None,
                "endAt": end_at.strftime("%Y/%m/%d")
                    if end_at else None
            }
        )["submissions"]
        return [
            FormSubmissionResponse.model_validate({
                **i, "name_map": name_mappings
            })
            for i in responses
        ]
    
    # @GHLClient.register_scope("forms.readonly")
    def iter_form_submissions(
        self,
        form_id: str|None = None,
        name_mappings: dict[str, str]|None = None,
        query: str|None = None,
        start_at: datetime|None = None,
        end_at: datetime|None = None
    ) -> Iterator[FormSubmissionResponse]:
        """
        Retrieves form submissions that match the criteria and returns
        them in a list of `FormSubmissionResponse`. Params are as the
        GHL API docs describe as. When `name_mappings` is passed, all
        returned form objects can reference their fields by the
        mapping. Note: ALL form objects will receive the same mapping,
        if multiple different forms are returned, leave blank and
        manually call `form.fields.set_name_map(mappings)`.
        """
        page = 1
        while True:
            submissions = self.get_form_submissions(
                form_id = form_id,
                name_mappings = name_mappings,
                page = page,
                limit = 20,
                query = query,
                start_at = start_at,
                end_at = end_at
            )
            if not submissions: break
            yield from submissions
            page += 1