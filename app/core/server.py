from os import environ
from flask import abort, request
from functools import wraps
from logging import error
from traceback import format_exception

from app.core.rich_error import RichException



def verify_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {environ["WEBHOOK_TOKEN"]}":
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def create_webhook(workflow_func):
    @verify_auth
    def webhook():
        try:
            ret = workflow_func() or {}
            ret.update({"success": True})
            return ret, 200
        except Exception as err:
            if isinstance(err, RichException):
                err_msg = str(err)
            else:
                err_msg = "".join(format_exception(err))
            error(err_msg)
            return {"success": False}, 200
    return webhook