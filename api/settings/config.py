from api.common import constants
from api.app import app
import os


class Config(object):
    DEBUG = False
    TESTING = False
    PORT = constants.PORT_DES
    GUARDIAN_SECRET_KEY = 'SuperSecretTruedat'
    SERVICE_TD_DQ = "http://localhost:4004"
    SERVICE_TD_AUTH = "http://localhost:4001"
    JWT_AUD = 'tdauth'
    ALGORITHM = 'HS512'
    EXTERNAL_HOST = 'localhost'
    EXTERNAL_PORT = 4009
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)
    VAULT_HOST = "http://localhost:4008"
    VAULT_TOKEN = "dead2687-ef0d-6ade-01b2-dec2ad244786"
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
    EXTERNAL_HOST = os.getenv('EXTERNAL_HOST', "localhost")
    EXTERNAL_PORT = os.getenv('EXTERNAL_PORT', 4009)
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)
    SERVICE_TD_DQ = os.getenv('SERVICE_TD_DQ', "http://localhost:4004")
    SERVICE_TD_AUTH = os.getenv('SERVICE_TD_AUTH', "http://localhost:4001")
    API_USERNAME = os.getenv('API_USERNAME', "api-admin")
    API_PASSWORD = os.getenv('API_PASSWORD', "xxxxxx")
    DB_USER = os.getenv('DB_USER', "postgres")
    DB_PASSWORD = os.getenv('DB_PASSWORD', "postgres")
    DB_NAME = os.getenv('DB_NAME', "td_qe_prod")
    DB_HOST = os.getenv('DB_HOST', "localhost")
    VAULT_TOKEN = os.getenv('VAULT_TOKEN', "319ee813-46f0-6153-a428-5a15ee5b4bdb")
    VAULT_HOST = os.getenv('VAULT_HOST', "http://localhost:8200")
    GUARDIAN_SECRET_KEY = os.getenv('GUARDIAN_SECRET_KEY', 'SuperSecretTruedat')
    SQLALCHEMY_DATABASE_URI="postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
        DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, DB_HOST=DB_HOST, DB_NAME=DB_NAME)


class DevelopmentConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    DEBUG = True
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + "/", "")


class TestingConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + "/", "")
    TESTING = True
    DEBUG = True
