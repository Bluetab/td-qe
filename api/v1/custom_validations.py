from api.model.entities.custom_validations_model import CustomValidationsModel
from api.v1.services.custom_validation import CustomValidation
from api.validation_json.validation import validate_schema
from api.v1.exceptions.invalid_usage import InvalidUsage
from flask import Blueprint, jsonify, request
from api.common.auth import auth
from flasgger import swag_from


custom_validations = Blueprint('custom_validations', __name__)


@custom_validations.route('/custom_validations', methods=['GET'])
@auth.login_required
@swag_from('swagger/custom_validation_index.yml')
def get_all_custom_validations():
    return jsonify({"data": [ custom_validation.to_dict()
                             for custom_validation in CustomValidationsModel.query.all() ] }), 200


@custom_validations.route('/custom_validations', methods=['POST'])
@auth.login_required
@validate_schema("custom_validation_schema")
@swag_from('swagger/custom_validation_create.yml')
def create_custom_validations():

    custom_validation_param = request.json["custom_validations"]

    CustomValidation.check_query(custom_validation_param)

    if CustomValidationsModel.find_by_implementation_key(
        custom_validation_param['implementation_key']):
        raise InvalidUsage('Rule {} already have a validation query'
                .format(custom_validation_param['implementation_key']),
                status_code=400)

    custom_validation = CustomValidationsModel(
        implementation_key=custom_validation_param["implementation_key"],
        query_validation=custom_validation_param["query_validation"])
    custom_validation.insert()

    return jsonify(custom_validation.to_dict()), 201


@custom_validations.route('/custom_validations/<int:custom_validation_id>', methods=['PUT'])
@auth.login_required
@validate_schema("custom_validation_schema")
@swag_from('swagger/custom_validation_modify.yml')
def update_custom_validations(custom_validation_id):

    custom_validation_param = request.json["custom_validations"]

    CustomValidation.check_query(custom_validation_param)

    custom_validation = CustomValidationsModel.find_by_custom_validation_id(custom_validation_id)
    if not custom_validation:
        raise InvalidUsage("Custom Validation {} not exits".format(
            custom_validation_id), status_code=400)

    if CustomValidationsModel.find_by_implementation_key(
        custom_validation_param['implementation_key']):
            raise InvalidUsage('Rule {} already have a validation query'
                .format(custom_validation_param['implementation_key']), status_code=400)

    custom_validation.implementation_key = custom_validation_param["implementation_key"]
    custom_validation.query_validation = custom_validation_param["query_validation"]
    custom_validation.insert()

    return jsonify(custom_validation.to_dict()), 200


@custom_validations.route('/custom_validations/<int:custom_validation_id>', methods=['DELETE'])
@auth.login_required
@swag_from('swagger/custom_validation_delete.yml')
def delete_custom_validations(custom_validation_id):

    custom_validation = CustomValidationsModel.find_by_custom_validation_id(custom_validation_id)
    if not custom_validation:
        raise InvalidUsage("Custom Validation {} not exits".format(
            custom_validation_id), status_code=400)
    custom_validation.delete()

    return "", 204
