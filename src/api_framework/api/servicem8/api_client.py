from api_framework.core.generic_client import BaseAPIClient
from .company_contact import CompanyContactAPI
from .job_materials import JobMaterialAPI
from .job_contacts import JobContactsApi
from .jobs import JobsAPI
from .notes import NotesAPI



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
        self.job_contacts = JobContactsApi(self)
        self.jobs = JobsAPI(self)
        self.notes = NotesAPI(self)
    
    def _get_auth(
        self,
        api_token: str
    ) -> str:
        return api_token