from pytest import fixture

from typing import Any



@fixture
def ghl_mock_record() -> dict[str, str|dict[str,str]|list[str]]:
    return {
        "id": "1234abcd5678efgh9012ijkl",
        "locationId": "1234abcd5678efgh9012ijkl",
        "objectId": "1234abcd5678efgh9012ijkl",
        "objectKey": "custom_objects.example",
        "createdBy": {
            "source": "workflow",
            "channel": "example channel",
            "sourceId": "123e4567-cfae-47bd-8501-23f94608521b",
            "createdAt": "2026-06-18T14:02:59.185Z"
        },
        "createdAt": "2026-06-18T14:02:59.185Z",
        "updatedAt": "2026-06-18T14:08:59.185Z",
        "owners": ["1234abcd5678efgh9012ijkl" for _ in range(5)],
        "followers": ["1234abcd5678efgh9012ijkl" for _ in range(5)],
        "properties": {"custom_field": "value"}
    }

@fixture
def ghl_mock_record_single_ret(
    ghl_mock_record: dict[str, str|dict[str,str]|list[str]]
) -> dict[str, Any]:
    return {
        "record": ghl_mock_record,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }

@fixture
def ghl_mock_record_list_ret(
    ghl_mock_record: dict[str, str|dict[str,str]|list[str]]
) -> dict[str, Any]:
    return {
        "records": [ghl_mock_record for _ in range(5)],
        "total": 5,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }