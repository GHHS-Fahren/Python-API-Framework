from importlib import import_module
from os import environ
from logging import info, error
from flask import Flask, abort, request



app = Flask(__name__)

def verify_auth(
        required_token: str
    ) -> None:
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {required_token}":
        print("Unauthorized access.")
        abort(403)

@app.post("/")
def webhook() -> None:
    verify_auth(environ["WEBHOOK_TOKEN"])

    info("Webhook has been triggered")
    print("Webhook has been triggered")
    module=import_module(f"app.workflows.{environ["WORKFLOW_NAME"]}")

    try:
        module.main()
        info("Webhook has completed successfully.")
        print("Webhook has completed successfully.")
        return {
            "success": True,
            "details": ""
        }, 200
    except Exception as e:
        print(f"Webhook has encountered an error.\n{e}")
        error(f"Webhook has encountered an error.\n{e}")
        return {
            "success": False,
            "details": str(e).replace("\n","<br>")
        }, 500
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = 8080
    )