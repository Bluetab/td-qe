from api.model.base_model import BaseModel, TimestampMixin, db


class CustomValidationsModel(BaseModel, TimestampMixin, db.Model):

    """Table of custom validations"""
    __tablename__ = 'custom_validations'
    implementation_key = db.Column(db.String(255))
    query_validation = db.Column(db.Text)


    @classmethod
    def find_by_implementation_key(cls, implementation_key):
        return cls.query.filter_by(implementation_key=implementation_key).first()


    @classmethod
    def find_by_custom_validation_id(cls, custom_validation_id):
        return cls.query.filter_by(id=custom_validation_id).first()


    def to_dict(self):
        return {'id': self.id, 'implementation_key': self.implementation_key,
                'query_validation': self.query_validation}
