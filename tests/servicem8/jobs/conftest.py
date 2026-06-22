from pytest import fixture



@fixture
def sm8_mock_job() -> dict[str, str|int|float]:
    return {
        "created_by_staff_uuid": "123e4567-cfae-47bd-8501-23f94608521b",
        "date": "2026-03-01 12:00:00",
        "company_uuid": "123e4567-a74c-4c4d-8102-23f94645565b",
        "billing_address": "",
        "status": "Work Order",
        "lng": 153.07005,
        "lat": -26.80588,
        "payment_date": "0000-00-00 00:00:00",
        "payment_actioned_by_uuid": "123e4567-4ac5-439d-9e29-23f9497c917b",
        "payment_method": "",
        "payment_amount": "50",
        "category_uuid": "123e4567-135d-4eda-9c30-23f9439ab09b",
        "payment_note": "",
        "geo_is_valid": 1,
        "purchase_order_number": "558",
        "invoice_sent": True,
        "invoice_sent_stamp": "2026-03-01 12:00:00",
        "ready_to_invoice": "1",
        "ready_to_invoice_stamp": "2026-03-01 12:00:00",
        "geo_country": "Australia",
        "geo_postcode": "4551",
        "geo_state": "QLD",
        "geo_city": "Baringa",
        "geo_street": "Hancock Way",
        "geo_number": "8/24-26",
        "queue_uuid": "123e4567-7677-49f2-b85f-23f946c0f0bb",
        "queue_expiry_date": "2026-03-01 12:00:00",
        "queue_assigned_staff_uuid": "123e4567-9b3a-4720-8f27-23f94b79908b",
        "badges": "[\"123e4567-9b3a-4720-8f27-23f94b79908b\",\"123e4567-9b3a-4720-8f27-23f94b79908b\"]",
        "quote_date": "2026-03-01 12:00:00",
        "quote_sent": False,
        "quote_sent_stamp": "0000-00-00 00:00:00",
        "work_order_date": "2026-03-01 12:00:00",
        "related_knowledge_articles": False,
        "uuid": "123e4567-8944-4763-8b13-23f9477acddb",
        "active": 1,
        "edit_date": "2026-03-01 12:00:00",
        "job_address": "8/24-26 Hancock Way,\nBaringa QLD 4551",
        "job_description": "",
        "work_done_description": "",
        "generated_job_id": "558",
        "total_invoice_amount": "5.5000",
        "payment_processed": 0,
        "payment_processed_stamp": "2026-03-01 12:00:00",
        "payment_received": 0,
        "payment_received_stamp": "2026-03-01 12:00:00",
        "completion_date": "2026-03-01 12:00:00",
        "completion_actioned_by_uuid": "123e4567-5acd-4f56-a123-23f94e9c86fb",
        "unsuccessful_date": "2026-03-01 12:00:00",
        "job_is_scheduled_until_stamp": "2026-03-01 12:00:00"
    }

@fixture
def sm8_mock_job_list(
    sm8_mock_job: dict[str, str|int|float],
    amount: int = 20
) -> list[dict[str, str|int|float]]:
    return [
        sm8_mock_job
        for _ in range(amount)
    ]