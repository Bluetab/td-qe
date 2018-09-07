from api.model.entities.custom_validations_model import CustomValidationsModel
from api.validation_json.validation import validate_schema
from api.common.utils import checkonlyone, abort
from flask import Blueprint, jsonify, request
from api.common.auth import auth
from sqlparse.sql import Statement, Identifier, IdentifierList
import sqlparse


custom_validations = Blueprint('custom_validations', __name__)


@custom_validations.route('/custom_validations', methods=['GET'])
@auth.login_required
def get_all_custom_validations():
    return jsonify({"data": [ custom_validation.to_dict()
                             for custom_validation in CustomValidationsModel.query.all() ] }), 200


@custom_validations.route('/custom_validations', methods=['POST'])
#@auth.login_required
@validate_schema('custom_validation_schema')
def create_custom_validations():

    custom_validation_param = request.json["custom_validations"]
    sql_tokens = sqlparse.parse(custom_validation_param["query_validation"])[0]

    if Statement(sql_tokens).get_type() != "SELECT" or Identifier(sql_tokens).is_wildcard():
        return abort(400, {'message': 'Not valid query'})

    if CustomValidationsModel.find_by_rule_id(custom_validation_param['rule_id']):
        return abort(400, {'message':
                           'Rule {} already have a validation query'
                           .format(custom_validation_param['rule_id'])})

    custom_validation = CustomValidationsModel(
        rule_id=custom_validation_param["rule_id"],
        query_validation=custom_validation_param["query_validation"])
    custom_validation.insert()

    return jsonify(custom_validation.to_dict()), 201


@custom_validations.route('/custom_validations/<int:custom_validation_id>', methods=['PUT'])
@auth.login_required
@validate_schema('custom_validation_schema')
def update_custom_validations(custom_validation_id):

    custom_validation_param = request.json["custom_validations"]
    sql_tokens = sqlparse.parse(custom_validation_param["query_validation"])[0]

    if Statement(sql_tokens).get_type() != "SELECT" or Identifier(sql_tokens).is_wildcard():
        return abort(400, {'message': 'Not valid query'})

    custom_validation = CustomValidationsModel.find_by_custom_validation_id(custom_validation_id)
    if not custom_validation:
        return abort(400, {'message': "Custom Validation {} not exits".format(custom_validation_id)})

    if CustomValidationsModel.find_by_rule_id(custom_validation_param['rule_id']):
        return abort(400, {'message':
                           'Rule {} already have a validation query'
                           .format(custom_validation_param['rule_id'])})

    custom_validation.rule_id = custom_validation_param["rule_id"]
    custom_validation.query_validation = custom_validation_param["query_validation"]
    custom_validation.insert()

    return jsonify(custom_validation.to_dict()), 201


@custom_validations.route('/custom_validations/<int:custom_validation_id>', methods=['DELETE'])
@auth.login_required
def delete_custom_validations(custom_validation_id):

    custom_validation = CustomValidationsModel.find_by_custom_validation_id(custom_validation_id)
    if not custom_validation:
        return abort(400, {'message': "Custom Validation {} not exits".format(custom_validation_id)})
    custom_validation.delete()

    return "", 204
