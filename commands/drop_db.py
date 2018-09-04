from sqlalchemy_utils import database_exists, drop_database
from api.app import app


if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    drop_database(app.config["SQLALCHEMY_DATABASE_URI"])
