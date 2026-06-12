from api_framework.core.generic_client import BaseAPIClient



class SM8Client(BaseAPIClient):
    def __init__(
        self,
        base_url: str,
        api_token: str
    ) -> None:
        super().__init__(base_url, api_token=api_token)
        self.session.headers.update({"X-API-Key": api_token})
    
    def _get_auth(
        self,
        api_token: str
    ) -> str:
        return api_token