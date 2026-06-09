from os import environ

from api_framework.core.generic_client import BaseAPIClient
from api_framework.api.gohighlevel.forms import FormAPI
from api_framework.api.gohighlevel.objects import CustomObjectRecordAPI
from api_framework.api.gohighlevel.relations import RelationsAPI
from api_framework.api.gohighlevel.sub_account import CustomFieldAPI
from api_framework.api.gohighlevel.messages import MessagesAPI



class GHLClient(BaseAPIClient):
    """
    Client class for interacting with the GoHighLevel API.
    """

    def __init__(
        self,
        base_url: str,
        location_id: str,
        api_token: str
    ) -> None:
        super().__init__(base_url, api_token=api_token)
        self.session.headers.update({"Version": "2023-02-21"})
        self.location_id = location_id

        self.forms = FormAPI(self)
        self.records = CustomObjectRecordAPI(self)
        self.relations = RelationsAPI(self)
        self.custom_fields = CustomFieldAPI(self)
        self.messages = MessagesAPI(self)
    
    def _get_auth(
            self,
            api_token: str
        ) -> str:
        return f"Bearer {api_token}"