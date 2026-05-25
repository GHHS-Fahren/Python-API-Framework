from importlib import import_module
from os import environ

module = import_module(f"app.servers.{environ['SERVER_NAME']}")
app = module.app

if __name__ == "__main__":
    from dotenv import load_dotenv
    if not ("WEBHOOK_TOKEN" in environ or "SERVER_NAME" in environ):
        load_dotenv()
    
    with app.test_client() as client:
        response = client.post(
            "/vehicle_log_submitted",
            headers = {
                "Authorization": f"Bearer {environ["WEBHOOK_TOKEN"]}"
            }
        )
        print(response.status_code)
        print(response.text)