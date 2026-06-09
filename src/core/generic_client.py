from requests import session
from urllib.parse import urljoin

from src.utils.rich_error import RichException



class BaseAPIClient:
    """
    Base class for retrieving data from an api endpoint. Not
    much will be held in here other than common funcs for
    the subclasses. Uses a request session to keep cookies
    persistant across multiple get/post requests.
    """

    def __init__(
            self,
            base_url: str,
            **auth_kwargs
        ) -> None:
        
        if not isinstance(base_url, str):
            raise TypeError("`base_url` is not a string!")
        
        self.base_url = base_url.removesuffix("/")
        self.session = session()
        self.session.headers.update({
            "Authorization": self._get_auth(**auth_kwargs),
            "Accept": "application/json"
        })
    
    def _get_auth(
            self,
            **kwargs
        ) -> str:
        """
        Subclasses must impliment the method to get the auth key
        """
        raise NotImplementedError(
            "Subclasses should have `_get_auth` implimented!"
        )
        
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
        response = self.session.request(
            method = method,
            url = urljoin(self.base_url, endpoint),
            params = params,
            json = json,
            data = data,
            files = files,
            headers = headers
        )
        if not response.ok:
            raise RichException(
                name = "HTTPError",
                message = f"{method} Failed",
                meta = {
                    "request_url": response.request.url,
                    "request_body": response.request.body,
                    "response_code": response.status_code,
                    "response_body": response.text
                }
            )

        content_type = response.headers.get("Content-Type")
        if "application/json" in content_type:
            return response.json()
        else:
            return response.content