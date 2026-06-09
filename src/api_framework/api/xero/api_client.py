from base64 import encode
from datetime import datetime, timedelta

from api_framework.core.generic_client import BaseAPIClient



class XeroClient(BaseAPIClient):
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        scopes: list[str]
    ) -> None:
        self.scopes = scopes
        self.client_id = client_id
        self.client_secret = client_secret

        super().__init__(base_url)


    def _get_auth(
        self
    ) -> str:
        response = self.request(
            "POST",
            "https://identity.xero.com/connect/token",
            headers = {
                "Content-Type":
                    "application/x-www-form-urlencoded",
                "authorization":
                    encode(f"{self.client_id}:{self.client_secret}")
            },
            data = {
                "grant_type": "client_credentials",
                "scope": " ".join(self.scopes)
            }
        )

        expires_in = timedelta(seconds = response["expires_in"])
        self._token_exp = datetime.now() + expires_in

        return f"Bearer {response["access_token"]}"
    
    def _refresh_auth(
        self
    ) -> None:
        self.session.headers.update({
            "Authorization": self._get_auth()
        })

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        json: dict | None = None,
        data = None,
        files: dict | None = None,
        headers: dict | None = None
    ) -> dict | bytes:
        """
        Thin wrapper for requests.request. Automatially throws an
        error if the request failed but otherwise returns dictionary
        if the response type is json, or return the content of the
        response if not.
        """
        if datetime.now() > self._token_exp:
            self._refresh_auth()
        super.request(
            method,
            endpoint,
            params = params,
            json = json,
            data = data,
            files = files,
            headers = headers
        )