from __future__ import annotations

from urllib.parse import quote

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
            "{:.4f}".format(data["quantity"]),
        "job_material_bundle_uuid":
            data.get("material_bundle_id"),
        "sort_order":
            None if data.get("cost") is None
            else str(data.get("sort_order")),
        "name":
            data.get("name"),
        "cost":
            None if data.get("cost") is None
            else str(data.get("cost")),
        "price":
            None if data.get("price") is None
            else str(data.get("price")),
        "tax_rate_uuid":
            data.get("tax_rate_id"),
        "displayed_cost":
            None if data.get("displayed_cost") is None
            else str(data.get("displayed_cost")),
        "displayed_amount":
            None if data.get("displayed_amount") is None
            else str(data.get("displayed_amount")),
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
        filters: str|None = None
    ) -> list[JobMaterialResponse]:
        url = "jobmaterial.json"
        if filters: url += f"?$filter={quote(filters)}"
        materials = self._api_client.request(
            "GET",
            url
        )
        return [
            JobMaterialResponse.model_validate(material)
            for material in materials
        ]
    
    def iter_search_materials(
        self,
        filters: str|None
    ) -> Iterator[JobMaterialResponse]:
        curr_cursor = -1
        url = "jobmaterial.json"
        if filters: url += f"?$filter={quote(filters)}"
        while True:
            materials, headers = self._api_client.request(
                "GET",
                url,
                return_headers = True,
                params = {"cursor": curr_cursor}
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
            f"jobmaterial/{job_material_id}.json"
        )
        return JobMaterialResponse.model_validate(material)

    def create_job_material(
        self,
        job_material_data: JobMaterialParams
    ) -> JobMaterialResponse:
        _, headers = self._api_client.request(
            "POST",
            "jobmaterial.json",
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
        _ = self._api_client.request(
            "POST",
            f"jobmaterial/{job_material_id}.json",
            return_headers = True,
            json = serialise_data(job_material_data)
        )
        return self.get_job_material(job_material_id)
    
    def delete_job_material(
        self,
        job_material_id: str
    ) -> bool:
        ret = self._api_client.request(
            "DELETE",
            f"jobmaterial/{job_material_id}.json"
        )
        return ret["message"] == "OK"