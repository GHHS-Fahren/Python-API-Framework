import pytest
from os import environ

from api_framework import GoHighLevel



ghl_client = GoHighLevel(
    base_url = "https://services.leadconnectorhq.com/",
    location_id = environ["GHL_LOC_ID"],
    api_token = environ["GHL_TOKEN"]
)
funcs = {
    ghl_client.estimates.search_estimates: {"limit": 1000},
    ghl_client.invoices.search_invoices: {"limit": 1000},
    ghl_client.transactions.search_transactions: {"limit": 1000}
    # ghl_client.estimates.search_templates: {"limit": 1000},
    # ghl_client.forms.get_form_submissions: {"limit": 1000},
    # ghl_client.records.search_records: {"limit": 1000, "object_key": "properties"}
}

@pytest.mark.parametrize(
    "func, kwargs",
    funcs.items()
)
def test_function(func, kwargs):
    # _ = func(**kwargs)
    for i in range(0, 10):
        _ = func(**{"limit": 1000, "offset": i*1000})