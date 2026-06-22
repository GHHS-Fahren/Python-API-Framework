from tests.conftest import (
    SM8_TEST_API_KEY as TEST_KEY, SM8_API_ENDPOINT as TEST_ENDPOINT
)
import pytest
from typing import TYPE_CHECKING
if TYPE_CHECKING: from api_framework import ServiceM8

class TestSM8ClientInit:
    def test_for_api_key(
        self,
        sm8_client: ServiceM8
    ):
        assert "X-Api-Key" in sm8_client.session.headers
        assert sm8_client.session.headers["X-Api-Key"] == TEST_KEY
    
    def test_for_base_url(
        self,
        sm8_client: ServiceM8
    ):
        assert sm8_client.base_url == TEST_ENDPOINT
    
    def test_for_raise_on_missing_base_url(
        self,
        sm8_client_class: type[ServiceM8]
    ):
        with pytest.raises(TypeError):
            _ = sm8_client_class(api_token = TEST_KEY) # pyright: ignore[reportCallIssue]
    
    def test_for_raise_on_missing_api_key(
        self,
        sm8_client_class: type[ServiceM8]
    ):
        with pytest.raises(TypeError):
            _ = sm8_client_class(base_url = TEST_ENDPOINT) # pyright: ignore[reportCallIssue]