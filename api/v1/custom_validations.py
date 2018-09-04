from api.model.entities.custom_validations_model import CustomValidationsModel
from api.validation_json.validation import validate_schema
from api.common.utils import checkonlyone, abort
from flask import Blueprint, jsonify, request
from api.common.auth import auth


custom_validations = Blueprint('custom_validations', __name__)


@custom_validations.route('/custom_validations', methods=['GET'])
@auth.login_required
def get_all_custom_validations():
    return jsonify({"data": [ custom_validation.to_dict()
                             for custom_validation in CustomValidationsModel.query.all() ] }), 200


@custom_validations.route('/custom_validations', methods=['POST'])
@auth.login_required
@validate_schema('custom_validation_schema')
def create_custom_validations():

    if CustomValidationsModel.find_by_quality_control_id(custom_validation_param['quality_control_id']):
        return abort(400, {'message':
                           'Quality Control {} already have a validation query'
                           .format(custom_validation_param['quality_control_id'])})

    custom_validation = CustomValidationsModel(
        quality_control_id=custom_validation_param["quality_control_id"],
        query_validation=custom_validation_param["query_validation"])
    custom_validation.save_to_db()

    return jsonify(custom_validation.to_dict()), 201
