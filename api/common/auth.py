from api.v1.exceptions.invalid_usage import InvalidUsage
from flask_httpauth import HTTPTokenAuth
from api.app import app
from flask import g
import jwt


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    if not token:
        return False
    data = verify_auth_token(token)
    if data:
        g.current_user = data
        return True
    return False


@auth.error_handler
def unauthorized():
    raise InvalidUsage('Unauthorized access', status_code=403)


def verify_auth_token(token):
    try:
        token = jwt.decode(token, app.config['GUARDIAN_SECRET_KEY'],
                           algorithms=app.config['ALGORITHM'],
                           audience=app.config['JWT_AUD'])
        if(token["is_admin"] != True):
            return None
    except jwt.ExpiredSignature:
        return None
    except jwt.DecodeError:
        return None
    return token
