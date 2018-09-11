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
    VAULT_TOKEN = "319ee813-46f0-6153-a428-5a15ee5b4bdb"
    VAULT_UNSEAL_KEY = "9093b7b40e8431cb86a5a03b6e998247eeb0398f0c0904227bd653a1c2bb488f"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_NAME = "td_qe_dev"
    DB_HOST = "localhost"
    SQLALCHEMY_DATABASE_URI="postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
        DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, DB_HOST=DB_HOST, DB_NAME=DB_NAME)
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
