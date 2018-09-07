from api.model.base_model import BaseModel, TimestampMixin, db


class CustomValidationsModel(BaseModel, TimestampMixin, db.Model):

    """Table of custom validations"""
    __tablename__ = 'custom_validations'
    rule_id = db.Column(db.Integer)
    query_validation = db.Column(db.Text)


    @classmethod
    def find_by_rule_id(self, rule_id):
        return self.query.filter_by(rule_id=rule_id).first()


    @classmethod
    def find_by_custom_validation_id(self, custom_validation_id):
        return self.query.filter_by(id=custom_validation_id).first()


    def to_dict(self):
        return {'id': self.id, 'rule_id': self.rule_id,
                'query_validation': self.query_validation}
