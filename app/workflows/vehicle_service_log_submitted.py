"""
---------------------- !!! IMPORTANT NOTICE !!! ----------------------
This code is a part of a larger project for GoHighLevel and other
platform API SDKs written in both python and javascript. Please do not
modify this code directly, instead push changes to the github repo and
push those changes downstream by either compiling the js and pasting
into the code block in an automation, or pushing changes to a cloud
run service.
---------------------- !!! IMPORTANT NOTICE !!! ----------------------

Due to limitations in being unable to create a new log from a form
submission without using custom object fields (as the form will
forcably require the id to be input before submitting) and limitations
on the code blocks (10MB memory which seems to run out when processing
raw file data), the code will be placed in a google cloud run instance
that triggers when a webhook is fired. GHL will send a webhook to the
google cloud run instance that holds no information that will be
parsed to the code.

The goals for this is to:
  1. Get latest form submission
  2. Find vehicle with provided registration
  3. Update associated vehicle with new service data
  4. Find company associated with the provided address
  4.1. Create company if not exists
  5. Create a new service log with provided details
  6. Upload attached image to service log
  7. Update service log to include image
  8. Assign the service log to associated vehicle
  9. Assign the service log to associated business

If any errors occur, an email should be sent to
  it_support@ghhomesafety.com.au
"""

from uuid import uuid4

from app.ghl.client import GHLClient
from app.ghl.objects.models import CustomObjectRequest
from app.core.file_models import RemoteImage



def filter_eq(key, val):
    return {
        "field": key,
        "operator": "eq",
        "value": val
    }

def main() -> None:
    ghl_client = GHLClient(
        base_url = "https://services.leadconnectorhq.com",
        location_id = "PoAqc6nsBdsQQIZA3WsX"
    )

    # 1. Get latest form submission
    name_mappings = {
        "vehicle_rego": "yJ4f26rQdnIn9FsF2igm",
        "service_date": "e5y42AONIMhKjcZP6Qzw",
        "sticker_date": "Z1hGblLR4gUkiHHIx7r1",
        "sticker_odom": "jQRmEeWd9y14UNc4kNyY",
        "vehicle_odom": "n3OXw4aq1iIG7qjeiGdv",
        "service_work": "xX2rQBm343iOeaFvUv9Z",
        "service_logs": "PISG4Pq6FA1yzC9dhkwJ",
        "service_note": "XhPzTkQFvs4vyZcPaoLW",
        "address": "address",
        "city": "city",
        "post_code": "postal_code",
        "state": "state",
        "country": "country"
    }
    form = ghl_client.forms.get_form_submissions(
        form_id = "1jXfQHJNMJhICyvlwtaw",
        name_mappings = name_mappings,
        limit = 1
    )[0]

    # 2. Find vehicle with associated registration
    filters = [{
        "field": "properties.vehicle_registration",
        "operator": "eq",
        "value": form.fields.get_by_name("vehicle_rego")
    }]
    vehicle = ghl_client.records.search_records(
        object_key = "custom_objects.vehicles",
        filters = filters,
        limit = 1
    )[0]

    # 3. Update associated vehicle with new service data
    record_data = {
        "properties": {
            "vehicle_odometer":
                int(form.fields.get_by_name("vehicle_odom")),
            "last_service_date":
                form.fields.get_by_name("service_date"),
            "last_service_odometer":
                int(form.fields.get_by_name("vehicle_odom")),
            "next_service_date":
                form.fields.get_by_name("sticker_date"),
            "next_service_odometer":
                int(form.fields.get_by_name("sticker_odom"))
        }
    }
    vehicle = ghl_client.records.update_record(
        object_key = vehicle.object_key,
        record_id = vehicle.id,
        record_data = CustomObjectRequest.model_validate(record_data)
    )

    # 4. Find company associated with the provided address
    filters = [
        filter_eq(
            "properties.address",
            form.fields.get_by_name("address")
        ),
        filter_eq(
            "properties.city",
            form.fields.get_by_name("city")
        ),
        filter_eq(
            "properties.postal_code",
            form.fields.get_by_name("post_code")
        ),
        filter_eq(
            "properties.state",
            form.fields.get_by_name("state")
        ),
    ]
    business = ghl_client.records.search_records(
        object_key = "custom_objects.businesses",
        filters = filters,
        limit = 1
    )
    if len(business) != 0: business = business[0]

    # 4.1 Create Business if not exists
    else:
        record_data = {
            "properties": {
                "business_name": "Unknown Business",
                "address": form.fields.get_by_name("address"),
                "city": form.fields.get_by_name("city"),
                "postal_code": form.fields.get_by_name("post_code"),
                "state": form.fields.get_by_name("state")
            }
        }
        business = ghl_client.records.create_record(
            object_key = "custom_objects.businesses",
            record_data =
                CustomObjectRequest.model_validate(record_data)
        )

    # 5. Create a new service log with provided details
    record_data = {
        "properties": {
            "log_id":
                str(uuid4()),
            "vehicle_registration":
                form.fields.get_by_name("vehicle_rego"),
            "service_date":
                form.fields.get_by_name("service_date"),
            "vehicle_odometer":
                int(form.fields.get_by_name("vehicle_odom")),
            "work_performed_on_vehicle":
                form.fields.get_by_name("service_work"),
            "service_notes":
                form.fields.get_by_name("service_note")
        }
    }
    service_log = ghl_client.records.create_record(
        object_key = "custom_objects.vehicle_service_logs",
        record_data = CustomObjectRequest.model_validate(record_data)
    )

    # 6. Upload attached image to service log
    images = {
        f"image_{k}": RemoteImage(v).compress_image()
        for k,v in enumerate(form.fields.get_by_name("service_logs"))
    }
    uploads = ghl_client.custom_fields.upload_to_custom_fields(
        field_id = service_log.id,
        files = images
    )

    # 7. Update service log to include image
    record_data = {
        "properties": {
            "images_of_vehicle_service_log": {
                "add": [{"url": url} for url in uploads.values()]
            }
        }
    }
    service_log = ghl_client.records.update_record(
        object_key = service_log.object_key,
        record_id = service_log.id,
        record_data = CustomObjectRequest.model_validate(record_data)
    )

    # 8. Assign the service log to associated vehicle
    relation = ghl_client.relations.create_relation(
        association_id = "6a138994e8d03912dc647e8b",
        first_record_id = service_log.id,
        second_record_id = vehicle.id
    )

    # 9. Assign the service log to associated business
    relation = ghl_client.relations.create_relation(
        association_id = "6a13e07931f2405231c8d802",
        first_record_id = business.id,
        second_record_id = service_log.id
    )

if __name__ == "__main__":
    main()