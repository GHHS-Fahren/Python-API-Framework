from pytest import fixture

from typing import Any



@fixture
def ghl_mock_attachment() -> dict[str, str|int]:
    return {
        "id": "6a2794b8dc7eb330de33361a",
        "name": "Example Name",
        "url":"https://example.com/document/6a2794b8dc7eb330de33361a",
        "type": "application/pdf",
        "size": 4586648
    }

@fixture
def ghl_mock_estimate_item_tax() -> dict[str, str|int]:
    return {
        "_id": "1234abcd5678efgh9012ijkl",
        "name": "TAX ",
        "rate": 5,
        "calculation": "exclusive",
        "description": "Trolling Tax",
        "taxId": "1234abcd5678efgh9012ijkl"
    }

@fixture
def ghl_mock_estimate_item(
    ghl_mock_estimate_item_tax: dict[str, str|int],
    ghl_mock_attachment: dict[str, str|int]
) -> dict[str, Any]:
    return {
        "taxes": [ghl_mock_estimate_item_tax],
        "taxInclusive": True,
        "attachments": [ghl_mock_attachment for _ in range(5)],
        "_id": "1234abcd5678efgh9012ijkl",
        "description": "<p>Example Description</p>",
        "currency": "DOUBLOONS",
        "productId": "1234abcd5678efgh9012ijkl",
        "priceId": "1234abcd5678efgh9012ijkl",
        "amount": 899,
        "qty": 5,
        "name": "Example Name",
        "type": "one_time"
    }

@fixture
def ghl_mock_address() -> dict[str, str]:
    return {
        "addressLine1": "Unit 3, 5 Example Street",
        "city": "Metropolis",
        "state": "STE",
        "countryCode": "om",
        "postalCode": "48379"
    }

@fixture
def ghl_mock_custom_value() -> dict[str, str]:
    return {
        "name": "Example Name",
        "fieldKey": "{{custom_values.example_name}}",
        "id": "6a2794b8dc7eb330de33361a",
        "value": "Example Value"
    }

@fixture
def ghl_mock_business_details(
    ghl_mock_address: dict[str, str],
    ghl_mock_custom_value: dict[str, str]
) -> dict[str, Any]:
    return {
        "logoUrl": "https://example.com/logo.png",
        "name": "Example Name",
        "address": ghl_mock_address,
        "phoneNo": "3472 8989 7324",
        "website": "https://example.com/",
        "customValues": [ghl_mock_custom_value for _ in range(5)]
    }

@fixture
def ghl_mock_estimate_contact(
    ghl_mock_address: dict[str, str]
) -> dict[str, Any]:
    return {
        "id": "6a2794b8dc7eb330de33361a",
        "name": "Jane Doe",
        "phoneNo": "3472 8989 7324",
        "email": "jane@example.com",
        "additionalEmails": [],
        "address": ghl_mock_address,
        "customFields": []
    }

@fixture
def ghl_mock_estimate(
    ghl_mock_estimate_item: dict[str, Any],
    ghl_mock_business_details: dict[str, Any],
    ghl_mock_estimate_contact: dict[str, Any],
    ghl_mock_attachment: dict[str, str|int]
) -> dict[str, Any]:
    return {
        "_id": "1234abcd5678efgh9012ijkl",
        "liveMode": True,
        "deleted": False,
        "estimateStatus": "sent",
        "altType": "location",
        "altId": "1234abcd5678efgh9012ijkl",
        "companyId": "1234abcd5678efgh9012ijkl",
        "discount": {
            "type": "fixed",
            "value": 299
        },
        "title": "Example Title",
        "name": "Example Name",
        "items": [ghl_mock_estimate_item for _ in range(5)],
        "sentBy": "1234abcd5678efgh9012ijkl",
        "issueDate": "2026-06-18T14:02:59.185Z",
        "expiryDate": "2026-07-18T14:02:59.185Z",
        "termsNotes": "<p>Example Terms & Conditions</p>",
        "businessDetails": ghl_mock_business_details,
        "contactDetails": ghl_mock_estimate_contact,
        "automaticTaxesCalculated": False,
        "meta": {
            "documentCreatedByTemplateId": "6a2794b8dc7eb330de33361a"
        },
        "estimateNumber": 3548,
        "updatedBy": "6a2794b8dc7eb330de33361a",
        "currency": "DOUBLOONS",
        "estimateActionHistory": [],
        "frequencySettings": {"enabled": False},
        "estimateNumberPrefix": "ESTIMATE-",
        "total": 899,
        "totalamountInUSD": 5137.4864,
        "attachments": [ghl_mock_attachment for _ in range(5)],
        "autoInvoice": {
            "enabled": False,
            "directPayments": False
        },
        "opportunityDetails": {
            "opportunityId":"6a2794b8dc7eb330de33361a"
        },
        "configuration": {"precision": 4},
        "createdAt": "2026-06-18T14:02:59.185Z",
        "updatedAt": "2026-06-18T14:08:59.185Z",
        "__v": 0,
        "automaticTaxesEnabled": None,
        "paymentScheduleConfig": None,
        "sentTo": {
            "email": ["jane@example.com"],
            "emailCc": [],
            "emailBcc": [],
            "phoneNo": ["3472 8989 7324"]
        },
        "currencyOptions": {
            "code": "DOUBLOONS",
            "symbol": "DB$"
        }
    }

@fixture
def ghl_mock_estimate_list_ret(
    ghl_mock_estimate: dict[str, Any]
) -> dict[str, Any]:
    return {
        "estimates": [ghl_mock_estimate for _ in range(5)],
        "total": 5,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }

@fixture
def ghl_mock_estimate_template(
    ghl_mock_estimate: dict[str, Any]
) -> dict[str, Any]:
    mock_data = {**ghl_mock_estimate}
    delete_list = [
        "estimateStatus", "companyId", "sentBy", "issueDate",
        "expiryDate", "contactDetails", "meta", "estimateNumber",
        "estimateActionHistory", "frequencySettings",
        "totalamountInUSD", "autoInvoice", "opportunityDetails",
        "automaticTaxesEnabled", "paymentScheduleConfig", "sentTo",
        "currencyOptions"
    ]
    for i in delete_list: del mock_data[i]
    return mock_data

@fixture
def ghl_mock_estimate_template_list_ret(
    ghl_mock_estimate_template: dict[str, Any]
) -> dict[str, Any]:
    return {
        "data": [ghl_mock_estimate_template for _ in range(5)],
        "total": 5,
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }