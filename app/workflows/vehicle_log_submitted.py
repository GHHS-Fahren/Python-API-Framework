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
parsed to the code. Should any errors occur, an email should be sent
to 

The goals for this is to:
  1. Get latest form submission
  2. Find vehicle with associated registration
  3. Create a new vehicle log with provided details
  4. Upload attached images to GHL (needs vehicle log id for upload)
  5. Update vehicle log to include images
  6. Assign the vehicle log to associated vehicle

If any errors occur, an email should be sent to
  it_support@ghhomesafety.com.au
"""

from uuid import uuid4
from datetime import datetime
from logging import info, error

from app.ghl.client import GHLClient
from app.ghl.objects.models import CustomObjectRequest
from app.core.file_models import RemoteImage



def main() -> None:
    ghl_client = GHLClient(
        base_url = "https://services.leadconnectorhq.com",
        location_id = "PoAqc6nsBdsQQIZA3WsX"
    )

    print("Retrieving form submission...")
    # Retrieving the form submission
    name_mappings = {
        "registration":   "J6YR0PTxfEn05h0Wd8p3",
        "odometer":       "lvyVhrV7BVu0qdzaRDzl",
        "photo_odometer": "OXpBvEpepcJjVOocLHel",
        "photo_front":    "X8tFtgR2ICCI0oTbIMG6",
        "photo_right":    "D94LPwMR7tSkeeLTkRpm",
        "photo_rear":     "zIsrEyoLFbDK61hnnWkd",
        "photo_left":     "NKBFd9XUkLLZ6tPO72Xm",
        "new_damage":     "yrEIF7cSMd4WnQKVVO9w",
        "notes":          "TfEIjkwY5PiY2NNapN9Q"
    }
    form = ghl_client.forms.get_form_submissions(
        form_id = "vmZ77ORes927yGfCeq3o",
        name_mappings = name_mappings,
        limit = 1
    )[0]

    print("Retrieving vehicle data...")
    # Retrieving the associated vehicle's data
    filters = [{
        "field": "properties.vehicle_registration",
        "operator": "eq",
        "value": form.fields.get_by_name("registration")
    }]
    vehicle = ghl_client.records.search_records(
        object_key = "custom_objects.vehicles",
        filters = filters,
        limit = 1
    )[0]

    print("Creating new vehicle log...")
    # Creating a new vehicle log
    record_data = {
        "properties": {
            "submission_id":
                str(uuid4()),
            "submission_date":
                datetime.now().strftime("%Y-%m-%d"),
            "submission_notes":
                form.fields.get_by_name("notes"),
            "vehicle_odometer":
                int(form.fields.get_by_name("odometer")),
            "vehicle_has_new_damage":
                form.fields.get_by_name("new_damage")
        }
    }
    vehicle_log = ghl_client.records.create_record(
        object_key = "custom_objects.vehicle_logs",
        record_data = CustomObjectRequest.model_validate(record_data)
    )

    print("Processing & uploading images...")
    # Uploading the images to the newly created vehicle log
    images = {
        "odometer":
            RemoteImage(
                form.fields.get_by_name("photo_odometer")[0]
            ).compress_image(),
        "front":
            RemoteImage(
                form.fields.get_by_name("photo_front")[0]
            ).compress_image(),
        "driver":
            RemoteImage(
                form.fields.get_by_name("photo_right")[0]
            ).compress_image(),
        "back":
            RemoteImage(
                form.fields.get_by_name("photo_rear")[0]
            ).compress_image(),
        "passenger":
            RemoteImage(
                form.fields.get_by_name("photo_left")[0]
            ).compress_image()
    }
    uploads = ghl_client.custom_fields.upload_to_custom_fields(
        field_id = vehicle_log.id,
        files = images
    )

    print("Updating vehicle log to include uploaded images...")
    # Update vehicle log to include uploaded files
    record_data = {
        "properties": {
            "vehicle_photo_odometer": {
                "add": [{"url":uploads["odometer"]}]
            },
            "vehicle_photo_front": {
                "add": [{"url":uploads["front"]}]
            },
            "vehicle_photo_driver_side": {
                "add": [{"url":uploads["driver"]}]
            },
            "vehicle_photo_back": {
                "add": [{"url":uploads["back"]}]
            },
            "vehicle_photo_passenger_side": {
                "add": [{"url":uploads["passenger"]}]
            },
        }
    }
    vehicle_log = ghl_client.records.update_record(
        object_key = vehicle_log.object_key,
        record_id = vehicle_log.id,
        record_data = CustomObjectRequest.model_validate(record_data)
    )

    print("Creating association between vehicle and vehicle log...")
    # Create association between vehicle and vehicle log
    relation = ghl_client.relations.create_relation(
        association_id = "69d72241a0b3ec4a65b0ae6e",
        first_record_id = vehicle_log.id,
        second_record_id = vehicle.id
    )

if __name__ == "__main__":
    main()