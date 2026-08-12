from __future__ import annotations

from api_framework.models.servicem8.job_contacts import (
    JobContactParams, JobContactResponse
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client



def serialise_data(data: JobContactParams) -> dict[str, str|None]:
    return {
        "job_uuid": data["job_id"],
        "type": data["type"],
        "first": data.get("first"),
        "last": data.get("last"),
        "phone": data.get("phone"),
        "mobile": data.get("mobile"),
        "email": data.get("email"),
    }

class JobContactsApi:
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client

    def get_job_contact(
        self,
        job_contact_id: str
    ) -> JobContactResponse:
        contact = self._api_client.request(
            "GET",
            f"jobcontact/{job_contact_id}.json"
        )
        return JobContactResponse.model_validate(contact)

    def create_job_contact(
        self,
        job_contact_data: JobContactParams
    ) -> JobContactResponse:
        _, headers = self._api_client.request(
            "POST",
            "jobcontact.json",
            return_headers=True,
            json=serialise_data(job_contact_data)
        )
        return self.get_job_contact(
            headers["x-record-uuid"]
        )