from pytest import fixture



@fixture
def sm8_mock_company_contact() -> dict[str, str|int]:
    return {
        "uuid": "123e4567-ea79-439e-8ccd-23f9412b198b",
        "company_uuid": "123e4567-a9a8-4d1d-b8de-23f9473ad6bb",
        "is_primary_contact": "1",
        "active": 1,
        "edit_date": "2026-03-01 12:00:00",
        "job_uuid": "123e4567-a9a8-4d1d-b8de-23f9473ad6bb",
        "first": "jane",
        "last": "doe",
        "phone": "",
        "mobile": "0412 345 678",
        "email": "jane.doe@test.com",
        "type": "JOB"
    }

@fixture
def sm8_mock_company_contact_list(
    sm8_mock_company_contact: dict[str, str|int],
    contact_amount: int = 20
) -> list[dict[str, str|int]]:
    return [
        sm8_mock_company_contact
        for _ in range(contact_amount)
    ]