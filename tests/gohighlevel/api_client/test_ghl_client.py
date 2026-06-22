from pytest import raises

from tests.conftest import (
    GHL_TEST_API_KEY, GHL_API_ENDPOINT, GHL_API_LOCATION
)

from typing import TYPE_CHECKING

if TYPE_CHECKING: from api_framework import GoHighLevel



class TestGHLClientInit:
    def test_for_api_key(
        self,
        ghl_client: GoHighLevel
    ):
        assert "Authorization" in ghl_client.session.headers
        assert ghl_client.session.headers["Authorization"] \
            == "Bearer "+GHL_TEST_API_KEY
    
    def test_for_base_url(
        self,
        ghl_client: GoHighLevel
    ):
        assert ghl_client.base_url == GHL_API_ENDPOINT
    
    def test_for_version_exists(
        self,
        ghl_client: GoHighLevel
    ):
        assert "Version" in ghl_client.session.headers
    
    def test_for_raise_on_missing_base_url(
        self,
        ghl_client_class: type[GoHighLevel]
    ):
        with raises(TypeError):
            _ = ghl_client_class(**{
                "location_id": GHL_API_LOCATION,
                "api_token": GHL_TEST_API_KEY
            })

    def test_for_raise_on_missing_location_id(
        self,
        ghl_client_class: type[GoHighLevel]
    ):
        with raises(TypeError):
            _ = ghl_client_class(**{
                "base_url": GHL_API_ENDPOINT,
                "api_token": GHL_TEST_API_KEY
            })

    def test_for_raise_on_missing_api_key(
        self,
        ghl_client_class: type[GoHighLevel]
    ):
        with raises(TypeError):
            _ = ghl_client_class(**{
                "base_url": GHL_API_ENDPOINT,
                "location_id": GHL_API_LOCATION,
            })