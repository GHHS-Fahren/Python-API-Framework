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
        abort(403)

@app.post("/")
def webhook() -> None:
    verify_auth(environ["WEBHOOK_TOKEN"])

    module=import_module(f"app.workflows.{environ["WORKFLOW_NAME"]}")

    try:
        info("Webhook initiated")
        module.main()
        info("Webhook completed")
        return {
            "success": True,
            "details": ""
        }, 200
    except Exception as e:
        return {
            "success": False,
            "details": str(e).replace("\n","<br>")
        }, 500
    
if __name__ == "__main__":
    # from dotenv import load_dotenv
    # load_dotenv()

    with app.test_client() as client:
        response = client.post(
            "/",
            headers = {
                "Authorization": f"Bearer {environ["WEBHOOK_TOKEN"]}"
            }
        )
        print(response.status_code)
        print(response.text)
    
    app.run(
        debug = True,
        use_debugger = False,
        use_reloader = False,
        host = "0.0.0.0",
        port = 8080
    )