from flask_httpauth import HTTPTokenAuth
from api.common.utils import abort
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
    return abort(403, {'error': 'Unauthorized access'})


def verify_auth_token(token):
    try:
        token = jwt.decode(token, app.config['SECRET_KEY'],
                           algorithms=app.config['ALGORITHM'],
                           audience=app.config['JWT_AUD'])
    except jwt.ExpiredSignature:
        return None
    except jwt.DecodeError:
        return None
    return token
