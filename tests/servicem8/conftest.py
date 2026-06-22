from pytest import fixture
from tests.conftest import (
    SM8_TEST_API_KEY, SM8_API_ENDPOINT
)
from api_framework import ServiceM8



@fixture
def sm8_client() -> ServiceM8:
    return ServiceM8(
        SM8_API_ENDPOINT,
        SM8_TEST_API_KEY
    )

@fixture
def sm8_client_class() -> type[ServiceM8]:
    return ServiceM8

@fixture
def sm8_mock_error() -> dict[str, str|int]:
    return {
        "errorCode": 401,
        "message": "Authorization Required"
    }