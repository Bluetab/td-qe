from api.v1.exceptions.invalid_usage import InvalidUsage
from jsonschema.exceptions import ValidationError
from api.validation_json import schemas
from flask import jsonify, request
from jsonschema import validate
from functools import wraps
from api.app import app


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if not request.is_json or not request.get_json(silent=True):
                msg = "payload must be a valid json"
                return jsonify({"error": msg}), 400
            try:
                validate(request.json, eval("schemas." + schema_name))
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator
