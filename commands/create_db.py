from sqlalchemy_utils import database_exists, create_database
from api.app import app


if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])
