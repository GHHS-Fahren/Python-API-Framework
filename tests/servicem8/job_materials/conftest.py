from pytest import fixture



@fixture
def sm8_mock_job_material() -> dict[str, str|int]:
    return {
        "uuid": "123e4567-74e3-4f64-b22f-23f94bbf232b",
        "active": 1,
        "edit_date": "2026-03-01 12:00:00",
        "job_uuid": "123e4567-baf5-48ae-813e-23f9401800cb",
        "material_uuid": "123e4567-baf5-48ae-813e-23f9401800cb",
        "name": "labour",
        "quantity": "1.5000",
        "price": "20.7000",
        "displayed_amount": "31.0500",
        "displayed_amount_is_tax_inclusive": "1",
        "tax_rate_uuid": "123e4567-dbcd-485a-8ae8-23f946e8852b",
        "sort_order": "0",
        "cost": "0.0000",
        "displayed_cost": "0.0000",
        "job_material_bundle_uuid": ""
    }

@fixture
def sm8_mock_job_material_list(
    sm8_mock_job_material: dict[str, str|int],
    amount: int = 20
) -> list[dict[str, str|int]]:
    return [
        sm8_mock_job_material
        for _ in range(amount)
    ]