from pytest import fixture



contact_note = dict[str, str|bool|list[dict[str,str]]]

@fixture
def ghl_mock_contact_note() -> contact_note:
    return {
        "id": "6a2794b8dc7eb330de33361a",
        "body": "<p style=\"margin:0px\"><span style=\"color: rgba(255,0,173,1) !important; color: rgba(255,0,173,1) !important\"><strong>test</strong></span></p>",
        "bodyText": "test",
        "userId": "6a2794b8dc7eb330de33361a",
        "dateAdded": "2026-07-18T14:02:59.185Z",
        "contactId": "6a2794b8dc7eb330de33361a",
        "pinned": False,
        "relations": [{
            "objectKey": "contact",
            "recordId": "6a2794b8dc7eb330de33361a"
        }]
    }

@fixture
def ghl_mock_contact_note_list_ret(
    ghl_mock_contact_note: contact_note
) -> dict[str, str|list[contact_note]]:
    return {
        "notes": [ghl_mock_contact_note for _ in range(5)],
        "traceId": "123e4567-cfae-47bd-8501-23f94608521b"
    }