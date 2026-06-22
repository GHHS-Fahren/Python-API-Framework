from pytest import fixture

from typing import Any



@fixture
def ghl_mock_opportunity_custom_fields() -> dict[str, str]:
    return {
        "id": "1234abcd5678efgh9012ijkl",
        "fieldValue": "test value"
    }

@fixture
def ghl_mock_opportunity(
    ghl_mock_opportunity_custom_fields: dict[str, str]
) -> dict[str, Any]:
    return {
        "id": "1234abcd5678efgh9012ijkl",
        "name": "Example Name",
        "monetaryValue": 159,
        "pipelineId": "1234abcd5678efgh9012ijkl",
        "pipelineStageId": "1234abcd5678efgh9012ijkl",
        "status": "open",
        "source": "Unknown",
        "lastStatusChangeAt": "2026-06-18T14:02:59.185Z",
        "lastStageChangeAt": "2026-06-18T14:08:59.185Z",
        "createdAt": "2026-06-18T14:02:59.185Z",
        "updatedAt": "2026-06-18T14:08:59.185Z",
        "contactId": "1234abcd5678efgh9012ijkl",
        "isAttribute": True,
        "internalSource": {
            "type": "CREATED",
            "id": "1234abcd5678efgh9012ijkl",
            "apiVersion": "v1",
            "channel": "test channel",
            "source": "workflow"
        },
        "locationId": "1234abcd5678efgh9012ijkl",
        "lastActionDate": "2026-06-18T14:02:59.185Z",
        "customFields": [ghl_mock_opportunity_custom_fields for _ in range(5)],
        "followers": ["1234abcd5678efgh9012ijkl" for _ in range(2)],
        "contact": {
            "id": "1234abcd5678efgh9012ijkl",
            "name": "jane doe",
            "email": "jane@example.com",
            "phone": "3472 8989 7324",
            "tags": ["test" for _ in range(5)],
            "followers": []
        },
    }

@fixture
def ghl_mock_opportunity_single_ret(
    ghl_mock_opportunity: dict[str, Any]
) -> dict[str, Any]:
    return {
        "opportunity": ghl_mock_opportunity,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }

@fixture
def ghl_mock_opportunity_list_ret(
    ghl_mock_opportunity: dict[str, Any]
) -> dict[str, Any]:
    return {
        "opportunities": [ghl_mock_opportunity for _ in range(5)],
        "total": 5,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }