from pytest import fixture

from typing import Any



@fixture
def ghl_mock_relation() -> dict[str, Any]:
    return {
        "id": "6a2794b8dc7eb330de33361a",
        "firstObjectKey": "6a2794b8dc7eb330de33361a",
        "firstRecordId": "6a2794b8dc7eb330de33361a",
        "secondObjectKey": "6a2794b8dc7eb330de33361a",
        "secondRecordId": "6a2794b8dc7eb330de33361a",
        "associationId": "6a2794b8dc7eb330de33361a",
        "primary": True,
        "locationId": "6a2794b8dc7eb330de33361a"
    }

@fixture
def ghl_mock_relation_list_ret(
    ghl_mock_relation: dict[str, Any]
) -> dict[str, Any]:
    return {
        "relations": [ghl_mock_relation for _ in range(5)],
        "total": 5,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }