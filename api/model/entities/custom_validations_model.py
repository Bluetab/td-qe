from api.model.base_model import BaseModel, TimestampMixin, db


class CustomValidationsModel(BaseModel, TimestampMixin, db.Model):

    """Table of custom validations"""
    __tablename__ = 'custom_validations'
    quality_control_id = db.Column(db.Integer)
    query_validation = db.Column(db.Text)


    @classmethod
    def find_by_quality_control_id(self, quality_control_id):
        return self.query.filter_by(quality_control_id=quality_control_id).first()


    @classmethod
    def find_by_custom_validation_id(self, custom_validation_id):
        return self.query.filter_by(id=custom_validation_id).first()


    def to_dict(self):
        return {'id': self.id, 'quality_control_id': self.quality_control_id,
                'query': self.query_validation}
