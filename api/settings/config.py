from api.common import constants
from api.app import app
import os


class Config(object):
    DEBUG = False
    TESTING = False
    PORT = constants.PORT_DES
    SECRET_KEY = 'SuperSecretTruedat'
    SERVICE_TD_DQ = "http://localhost:4004"
    SERVICE_TD_AUTH = "http://localhost:4001"
    JWT_AUD = 'tdauth'
    ALGORITHM = 'HS512'
    EXTERNAL_HOST = 'localhost'
    EXTERNAL_PORT = 4009
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)
    VAULT_HOST = "http://localhost:4008"
    VAULT_TOKEN = "5e437b1b-2b96-697a-ef34-ac04186c888c"
    API_USERNAME = "api-admin"
    API_PASSWORD = "apipass"

class ProductionConfig(Config):
    APPLICATION_ROOT = '/home/ec2-user/td_qe'
    PORT = constants.PORT_PRO
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + "/", "")
    EXTERNAL_HOST = 'truedat.bluetab.net'
    EXTERNAL_PORT = 8008
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)
    API_USERNAME = "api-admin"
    API_PASSWORD = "xxxxxx"


class DevelopmentConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    DEBUG = True
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + "/", "")


class TestingConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + "/", "")
    TESTING = True
    DEBUG = True
