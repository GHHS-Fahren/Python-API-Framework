from pytest import fixture



@fixture
def sm8_mock_job_contact() -> dict[str, str|int]:
    return {
        "edit_date": "2026-03-01 12:00:00",
        "active": 1,
        "job_uuid": "123e4567-74e3-4f64-b22f-23f94bbf232b",
        "first": "Amber",
        "last": "Bradshaw",
        "email": "amber.bradshaw@example.com",
        "phone": "",
        "mobile": "0412345678",
        "type": "BILLING",
        "uuid": "123e4567-74e3-4f64-b22f-23f94bbf232b"
    }