from __future__ import annotations

from api_framework.models.servicem8.job_materials import (
    JobMaterialResponse, JobMaterialParams
)

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client
    from collections.abc import Iterator



def serialise_data(data: JobMaterialParams) -> dict[str, Any]:
    is_tax_inclusive = data.get(
        "is_displayed_tax_inclusive"
    )
    return {
        "job_uuid":
            data["job_id"],
        "material_uuid":
            data["material_id"],
        "quantity":
            str(data["quantity"]),
        "job_material_bundle_uuid":
            data.get("material_bundle_id"),
        "sort_order":
            str(data.get("sort_order")),
        "name":
            data.get("name"),
        "cost":
            str(data.get("cost")),
        "price":
            str(data.get("price")),
        "tax_rate_uuid":
            data.get("tax_rate_id"),
        "displayed_cost":
            str(data.get("displayed_cost")),
        "displayed_amount":
            str(data.get("displayed_amount")),
        "displayed_amount_is_tax_inclusive":
            None if is_tax_inclusive is None
            else str(int(is_tax_inclusive))
    }

class JobMaterialAPI():
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client
    
    def search_materials(
        self,
        filters: str
    ) -> list[JobMaterialResponse]:
        materials = self._api_client.request(
            "GET",
            "/jobmaterial.json",
            params = {
                "filter": filters
            }
        )
        return [
            JobMaterialResponse.model_validate(material)
            for material in materials
        ]
    
    def iter_search_materials(
        self,
        filters: str
    ) -> Iterator[JobMaterialResponse]:
        curr_cursor = -1
        while True:
            materials, headers = self._api_client.request(
                "GET",
                "/jobmaterial.json",
                return_headers = True,
                params = {
                    "filter": filters,
                    "cursor": curr_cursor
                }
            )
            curr_cursor = headers.get("x-next-cursor")
            if curr_cursor is None: break
            yield from [
                JobMaterialResponse.model_validate(i)
                for i in materials
            ]
    
    def get_job_material(
        self,
        job_material_id: str
    ) -> JobMaterialResponse:
        material = self._api_client.request(
            "GET",
            f"/jobmaterial/{job_material_id}.json"
        )
        return JobMaterialResponse.model_validate(material)

    def create_job_material(
        self,
        job_material_data: JobMaterialParams
    ) -> JobMaterialResponse:
        is_tax_inclusive = job_material_data.get(
            "is_displayed_tax_inclusive"
        )
        _, headers = self._api_client.request(
            "POST",
            "/jobmaterial.json",
            return_headers = True,
            json = serialise_data(job_material_data)
        )
        return self.get_job_material(
            headers["x-record-uuid"]
        )
    
    def update_job_material(
        self,
        job_material_id: str,
        job_material_data: JobMaterialParams
    ) -> JobMaterialResponse:
        _, headers = self._api_client.request(
            "POST",
            f"/jobmaterial/{job_material_id}.json",
            return_headers = True,
            json = serialise_data(job_material_data)
        )
        return self.get_job_material(
            headers["x-record-uuid"]
        )
    
    def delete_job_material(
        self,
        job_material_id: str
    ) -> bool:
        ret = self._api_client.request(
            "DELETE",
            f"/jobmaterial/{job_material_id}.json"
        )
        return ret["message"] == "OK"