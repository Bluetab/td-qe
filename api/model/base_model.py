from sqlalchemy.ext.declarative import declared_attr, as_declarative
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class TimestampMixin(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    @declared_attr
    def created_on(cls):
        return db.Column(db.DateTime, default=db.func.now())

    @declared_attr
    def updated_on(cls):
        return db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
