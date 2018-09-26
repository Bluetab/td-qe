from api.validation_json.validation import validate_schema
from api.v1.exceptions.invalid_usage import InvalidUsage
from api.v1.services.engine import Engine
from flask import Blueprint, request
from api.common.auth import auth
from api.common import constants
from flasgger import swag_from


engine = Blueprint('engine', __name__)

@engine.route('/engine/execute', methods=['POST'])
@auth.login_required
@validate_schema("tags_validation_schema")
@swag_from('swagger/engine_execute_index.yml')
def all_rules():

    rule_tags = request.json["rule_tags"] if request.json["rule_tags"] else None

    data = Engine.get_data_from_dq(constants.GET_RULE_IMPLEMENTATIONS,
        status=constants.VALID_EXEC_STATUS, rule_tags=rule_tags)

    status_code = Engine.execute_rules_quality(data)
    if status_code != 200:
        raise InvalidUsage("unprocessable entity", status_code=422)
    return "", 204


@engine.route('/engine/<int:business_concept_id>/execute', methods=['POST'])
@auth.login_required
@validate_schema('tags_validation_schema')
@swag_from('swagger/engine_business_execute.yml')
def rules_by_id(business_concept_id):

    rule_tags = request.json["rule_tags"] if request.json["rule_tags"] else None

    data = Engine.get_data_from_dq(
        constants.GET_RULE_IMPLEMENTATIONS_BY_BUSINESS_CONCEPT,
        business_concept_id,
        constants.VALID_EXEC_STATUS, rule_tags)

    status_code = Engine.execute_rules_quality(data)
    if status_code != 200:
        raise InvalidUsage("unprocessable entity", status_code=422)
    return "", 204
