from requests import session
from urllib.parse import urljoin

from api_framework.utils.rich_error import RichException

from typing import Any, Literal, overload



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
        # This specifically targets servicem8 that likes to return
        # created object's uuids through the headers 😭
        self.REUQEST_INJECT_HEADERS: list[str] = []
    
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
    
    @overload
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        return_headers: Literal[True],
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: str | None = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any] | bytes, dict[str, str]]: ...

    @overload
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        return_headers: Literal[False] = ...,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: str | None = None,
        files: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> dict[str, Any] | bytes: ...

    def request(
            self,
            method: str,
            endpoint: str,
            *,
            return_headers: bool = False,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
            data: str|None = None,
            files: dict[str, Any] | None = None,
            headers: dict[str, Any] | None = None
    ) -> tuple[dict[str,Any]|bytes,dict[str,str]]|dict[str,Any]|bytes:
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

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            if not return_headers:
                return response.json()
            return response.json(), dict(response.headers)
        else:
            if not return_headers:
                return response.content
            return response.content, dict(response.headers)