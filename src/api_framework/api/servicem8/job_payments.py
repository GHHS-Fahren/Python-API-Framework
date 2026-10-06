from __future__ import annotations

from urllib.parse import quote

from api_framework.models.servicem8.job_materials import JobMaterialResponse
from api_framework.models.servicem8.job_payments import (
    JobPaymentResponse, JobPaymentParams
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework.api.servicem8.api_client import SM8Client



class JobPaymentsAPI():
    def __init__(
        self,
        api_client: SM8Client
    ) -> None:
        self._api_client = api_client

    def search_payments(
        self,
        filters: str | None = None
    ):
        url = "jobpayment.json"
        if filters: url += f"?$filter={quote(filters)}"
        payments = self._api_client.request(
            "GET",
            url
        )
        return [
            JobPaymentResponse.model_validate(p)
            for p in payments
        ]
    
    def get_payment(
        self,
        payment_id: str
    ):
        payment = self._api_client.request(
            "GET",
            f"jobpayment/{payment_id}.json"
        )
        return JobMaterialResponse.model_validate(payment)
    
    def create_payment(
        self,
        payment_data: JobPaymentParams
    ):
        _, headers = self._api_client.request(
            "POST",
            "jobpayment.json",
            json={
                "job_uuid": payment_data["job_id"],
                "actioned_by_uuid": payment_data.get("actioned_by"),
                "timestamp": payment_data.get("paid_at"),
                "amount": str(round(
                    payment_data["amount"],4
                )),
                "method": payment_data.get("method"),
                "note": payment_data.get("note"),
                "attachment_uuid": payment_data.get("attachment_id")
            },
            return_headers=True,
        )
        return self.get_payment(
            headers["x-record-uuid"]
        )