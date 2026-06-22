from requests import session
from urllib.parse import urljoin, urlencode, quote, quote_plus

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
        if not base_url.endswith("/"): base_url += "/"
        self.base_url = base_url
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
    
    @overload
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        delete_empty: bool = True,
        use_quote_plus: bool = False,
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
        delete_empty: bool = True,
        use_quote_plus: bool = False,
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
            delete_empty: bool = True,
            use_quote_plus: bool = False,
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
        url = endpoint.removeprefix("/")
        if params:
            if delete_empty:
                params = {
                    k: v
                    for k,v in params.items()
                    if v is not None
                }
            url += "?" + urlencode(
                query=params,
                quote_via=quote_plus if use_quote_plus else quote
            )
        if delete_empty and json is not None:
            json = {
                k: v
                for k,v in json.items()
                if v is not None
            }
        response = self.session.request(
            method = method,
            url = urljoin(
                base=self.base_url,
                url=url
            ),
            # params = params,
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