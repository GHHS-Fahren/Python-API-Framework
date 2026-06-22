from __future__ import annotations

from api_framework.models.common.address import FrozenAddress
from api_framework.models.servicem8.jobs import JobResponse, JobParams

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client



class JobsAPI():
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client

    def get_job(
        self,
        job_id: str
    ) -> JobResponse:
        job = self._api_client.request(
            "GET",
            f"job/{job_id}.json"
        )
        return JobResponse.model_validate(job)
    
    def create_from_template(
        self,
        template_id: str,
        *,
        description: str|None = None,
        company_id: str|None = None,
        company_name: str|None = None,
        address: str|None = None
    ) -> JobResponse:
        job_ref = self._api_client.request(
            "POST",
            f"jobtemplate/{template_id}/job.json",
            json = {
                "job_description": description,
                "company_uuid": company_id,
                "company_name": None if company_id else company_name,
                "job_address": address
            }
        )
        return self.get_job(job_ref["jobUUID"])
    
    def create_job(self) -> None:
        raise NotImplementedError("Aint gotten to this yet 😔")

    def update_job(
        self,
        job_id: str,
        job_data: JobParams
    ) -> JobResponse:
        address=job_data.get("address") or FrozenAddress()
        _ = self._api_client.request(
            "POST",
            f"job/{job_id}.json",
            json = {
                "company_uuid": job_data.get("company", None),
                "category_uuid": job_data.get("category", None),
                "queue_uuid": job_data.get("queue", None),
                "status": job_data.get("status", None),
                "billing_address": job_data.get("billing_address", None),
                "job_description": job_data.get("description", None),
                "work_done_description": job_data.get("work_done", None),
                "badges": job_data.get("badges", None),
                "lat": address.latitude,
                "lng": address.longitude,
                "geo_number": address.number,
                "geo_street": address.street,
                "geo_city": address.city,
                "geo_state": address.state,
                "geo_postcode": address.postcode,
                "geo_country": address.country,
                "job_address": address.full_address,
            }
        )
        return self.get_job(job_id)