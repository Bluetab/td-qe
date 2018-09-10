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
    VAULT_TOKEN = "54c221be-0555-4492-2559-cda66aea33f8"
    VAULT_UNSEAL_KEY = "af37b7102129710e3b9af68afe33275578c092da667e7d3bb813cd60b3d1ee38"
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
