from os import environ

from app.core.generic_client import BaseAPIClient
from app.ghl.forms.api import FormAPI
from app.ghl.objects.api import CustomObjectRecordAPI
from app.ghl.relations.api import RelationsAPI
from app.ghl.sub_account.api import CustomFieldAPI



class GHLClient(BaseAPIClient):
    """
    Client class for interacting with the GoHighLevel API.
    """

    def __init__(
            self,
            base_url: str,
            location_id: str,
            **auth_kwargs
        ) -> None:
        super().__init__(base_url, **auth_kwargs)
        self.session.headers.update({"Version": "2023-02-21"})
        self.location_id = location_id

        self.forms = FormAPI(self)
        self.records = CustomObjectRecordAPI(self)
        self.relations = RelationsAPI(self)
        self.custom_fields = CustomFieldAPI(self)
    
    def _get_auth(
            self,
            **kwargs
        ) -> str:
        return f"Bearer {environ["GHL_TOKEN"]}"
    
    # @classmethod
    # def register_scope(
    #         *scopes: str
    #     ):
    #     """
    #     This decorator defines the scope or scopes a particular request
    #     is needed.
    #     """
    #     def decorator(func):
    #         func.registered_scopes = set(scopes)
    #         return func
    #     return decorator