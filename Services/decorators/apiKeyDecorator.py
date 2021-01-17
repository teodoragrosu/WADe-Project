from functools import wraps
import json
from flask import request
from flask_restful import abort

keys = []

with open("../Services/decorators/apiKeys.json", "r") as keyFile:
    keys = json.load(keyFile)


def match_api_keys(key, ip):
    return key in keys


def require_app_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if match_api_keys(request.args.get('apiKey'), request.remote_addr):
            return f(*args, **kwargs)
        else:
            abort(401)

    return decorated
