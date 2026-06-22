from pytest import fixture
from tests.conftest import (
    GHL_TEST_API_KEY, GHL_API_ENDPOINT, GHL_API_LOCATION
)
from api_framework import GoHighLevel



@fixture
def ghl_client() -> GoHighLevel:
    return GoHighLevel(
        base_url = GHL_API_ENDPOINT,
        api_token = GHL_TEST_API_KEY,
        location_id = GHL_API_LOCATION
    )

@fixture
def ghl_client_class() -> type[GoHighLevel]:
    return GoHighLevel

@fixture
def ghl_mock_error() -> dict[str, str|int]:
    return {
        "statusCode": 401,
        "message": "Invalid token: access is invalid",
        "error": "Unauthorized"
    }