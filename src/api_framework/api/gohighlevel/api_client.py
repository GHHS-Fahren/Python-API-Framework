from api_framework.core.generic_client import BaseAPIClient
from .forms import FormAPI
from .objects import CustomObjectRecordAPI
from .relations import RelationsAPI
from .sub_account import CustomFieldAPI
from .messages import MessagesAPI
from .estimates import EstimatesAPI
from .opportunities import OpportunitiesAPI
from .contacts import ContactsAPI



class GHLClient(BaseAPIClient):
    """
    The client class for interacting with the GoHighLevel API. Init
    requires the base api url, the location id that the client will be
    working in, and the token string without the "Bearer " at the
    start. If a cross location automation is needed, initiate two
    clients in different variables. The individual endpoints are
    exposed via variables in the class.
    """

    location_id: str
    forms: FormAPI
    records: CustomObjectRecordAPI
    relations: RelationsAPI
    custom_fields: CustomFieldAPI
    messages: MessagesAPI
    estimates: EstimatesAPI
    opportunities: OpportunitiesAPI
    contacts: ContactsAPI

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
        self.estimates = EstimatesAPI(self)
        self.opportunities = OpportunitiesAPI(self)
        self.contacts = ContactsAPI(self)
    
    def _get_auth(
            self,
            api_token: str
        ) -> str:
        return f"Bearer {api_token}"