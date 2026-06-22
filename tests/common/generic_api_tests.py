from json import loads
from urllib.parse import urljoin
from requests import HTTPError
import pytest, responses
from typing import Any, Callable

from api_framework.utils import RichException



class ValuePath:
    def __init__(self, path: str) -> None: self.path: str = path
    def get_value(self, data: Any) -> Any:
        node = data
        for seg in self.path.split("."):
            if not seg: continue
            if seg.lstrip("-").isdigit(): node = node[int(seg)]
            elif hasattr(node, seg): node = getattr(node, seg)
            else: node = node[seg]
            if callable(node): node = node()
        return node

class BaseApiEndpointTests:
    endpoint_base: str
    expected_requests: list[dict[str, Any]]
    request_responses: list[dict[str, Any]]
    failure_response: dict[str, Any]
    success_assertions: list[dict[str, Any]]
    func_reference = Callable[..., Any]
    func_kwargs: dict[str, Any]

    @pytest.fixture(autouse = True)
    def setup(self) -> None:
        raise NotImplementedError("Subclasses must impliment setup")

    def build_url(self, url: str) -> str:
        return urljoin(base=self.endpoint_base, url=url)

    def build_generic_asserts(
        self,
        obj_inst: tuple[str, type],
        req_field: tuple[str, Any],
    ) -> list[dict[str, Any]]:
        return [
            {
                "op": "inst",
                "vals": [ValuePath(obj_inst[0]), obj_inst[1]]
            }, {
                "op": "eq",
                "vals": [ValuePath(req_field[0]), req_field[1]]
            }
        ]
    
    def build_list_generic_asserts(
        self,
        obj_inst: tuple[str, type],
        req_field: tuple[str, Any],
    ) -> list[dict[str, Any]]:
        return [
            {
                "op": "inst",
                "vals": [ValuePath(""), list]
            }, {
                "op": "gt",
                "vals": [ValuePath("__len__"), 0]
            }
        ] + self.build_generic_asserts(
            obj_inst = ("0."+obj_inst[0], obj_inst[1]),
            req_field = ("0."+req_field[0], req_field[1])
        )

    def _parse_params(
        self,
        url: str
    ) -> dict[str, str]:
        params = url.split("?")[-1]
        
        ret_dict = {}
        for i in params.split("&"):
            k, v = i.split("=")
            if v.isdigit(): v = int(v)
            ret_dict[k] = v
        return ret_dict

    def _add_response(
        self,
        request_data: dict[str, Any],
        resp_status: int
    ) -> None:
        _ = responses.add(
            **request_data,
            status = resp_status
        )
    
    @responses.activate
    def _run_func(
        self,
        resp_status: int,
        request_responses: list[dict[str, Any]]|None = None,
        func_kwargs: dict[str, Any]|None = None
    ) -> tuple[Any, list[Any]]:
        request_responses = request_responses or self.request_responses
        func_kwargs = func_kwargs or self.func_kwargs
        for response in request_responses:
            self._add_response(response, resp_status)
        return self.func_reference(**func_kwargs), list(responses.calls)

    def _assertion_test(
        self,
        assertion_data: dict[str, Any],
        result: Any
    ) -> None:
        val1, val2 = assertion_data["vals"]
        if isinstance(val1,ValuePath):
            val1=val1.get_value(result)
        if isinstance(val2,ValuePath):val2=val2.get_value(result)
        match assertion_data["op"]:
            case "eq": assert val1 == val2
            case "gt": assert val1 > val2
            case "is": assert val1 is val2
            case "in": assert val1 in val2
            case "inst": assert isinstance(val1, val2)
    
    def request_test(self, request, expected) -> None:
        if "params" in expected:
            assert request.url.split("?")[0] == expected["url"]
            debug = self._parse_params(request.url)
            assert self._parse_params(request.url)==expected["params"]
        else:
            assert request.url == expected["url"]
        if "json" in expected:
            debug = loads(request.body)
            assert loads(request.body) == expected["json"]
        elif "body" in expected:
            assert request.body == expected["body"]
        if "headers" in expected:
            for name,value in expected["headers"].items():
                assert name in request.headers
                assert request.headers[name] == value

    
    def test_for_request_building(
        self,
        func_kwargs: dict[str, Any]|None = None,
        expected_requests: list[dict[str, Any]]|None = None,
        request_responses: list[dict[str, Any]]|None = None,
    ):
        expected_requests = expected_requests or self.expected_requests
        _, calls = self._run_func(200, request_responses, func_kwargs)
        requests = [i.request for i in calls]
        for i, request in enumerate(requests):
            self.request_test(request, expected_requests[i])

    def test_for_success(self):
        result, _ = self._run_func(200, self.request_responses)
        for assertion_data in self.success_assertions:
            self._assertion_test(assertion_data, result)
    
    def test_for_fail(self):
        request_responses: list[dict[str, Any]] = [{
            **self.request_responses[0],
            "json": self.failure_response
        }]
        with pytest.raises((HTTPError, RichException)):
            _ = self._run_func(401, request_responses)