from api.model.base_model import BaseModel, TimestampMixin, db


class CustomValidationsModel(BaseModel, TimestampMixin, db.Model):

    """Table of custom validations"""
    __tablename__ = 'custom_validations'
    rule_implementation_id = db.Column(db.Integer)
    query_validation = db.Column(db.Text)


    @classmethod
    def find_by_rule_implementation_id(cls, rule_implementation_id):
        return cls.query.filter_by(rule_implementation_id=rule_implementation_id).first()


    @classmethod
    def find_by_custom_validation_id(cls, custom_validation_id):
        return cls.query.filter_by(id=custom_validation_id).first()


    def to_dict(self):
        return {'id': self.id, 'rule_implementation_id': self.rule_implementation_id,
                'query_validation': self.query_validation}
