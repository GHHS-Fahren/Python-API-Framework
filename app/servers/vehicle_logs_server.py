from flask import Flask

from app.core.server import create_webhook
from app.workflows.vehicle_log_submitted \
    import main as submit_log
from app.workflows.vehicle_service_log_submitted \
    import main as submit_service



app = Flask(__name__)

app.post(
    "/vehicle_log_submitted",
    endpoint = "vehicle_log_submitted"
)(create_webhook(submit_log))
app.post(
    "/vehicle_service_submitted",
    endpoint = "vehicle_service_submitted"
)(create_webhook(submit_service))