from api_framework.core.generic_client import BaseAPIClient
from .company_contact import CompanyContactAPI
from .job_materials import JobMaterialAPI
from .jobs import JobsAPI



class SM8Client(BaseAPIClient):
    def __init__(
        self,
        base_url: str,
        api_token: str
    ) -> None:
        super().__init__(base_url, api_token=api_token)
        self.session.headers.update({"X-Api-Key": api_token})

        self.company_contacts= CompanyContactAPI(self)
        self.job_materials = JobMaterialAPI(self)
        self.jobs = JobsAPI(self)
    
    def _get_auth(
        self,
        api_token: str
    ) -> str:
        return api_token