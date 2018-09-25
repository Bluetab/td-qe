from api.common.utils import send_data_to_dq_results, writeDictToCSV, abort
from api.common import constants
from api.v1.services.rules import Rules
from api.validation_json.validation import validate_schema
from flask import Blueprint, request
from api.common.auth import auth
from api.common import vault
import importlib
import datetime



engine = Blueprint('engine', __name__)

@engine.route('/engine/execute', methods=['POST'])
@auth.login_required
@validate_schema("tags_validation_schema")
def all_rules():

    rule_tags = request.json["rule_tags"]

    data = Rules.get_data_from_dq(constants.GET_RULE_IMPLEMENTATIONS,
        status=constants.VALID_EXEC_STATUS, rule_tags=rule_tags)

    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


@engine.route('/engine/<int:business_concept_id>/execute', methods=['POST'])
@auth.login_required
@validate_schema("tags_validation_schema")
def rules_by_id(business_concept_id):

    rule_tags = request.json["rule_tags"]
    
    data = Rules.get_data_from_dq(
        constants.GET_RULE_IMPLEMENTATIONS_BY_BUSINESS_CONCEPT,
        business_concept_id,
        constants.VALID_EXEC_STATUS,
        rule_tags
    )

    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


def execute_rules_quality(data):
    rule_implementations = Rules.parse_rule_implementations(data)

    queries_ids_info = []
    for rule_implementation in rule_implementations:
        keys = vault.get_data_from_vault(constants.PATH_VAULT_SOURCES +
                                         rule_implementation["system"])

        if keys != None:
            query = Rules.get_query_by_type(rule_implementation)
            module = importlib.import_module(constants.API_DATABASE_PATH +
                                             keys.pop("connection_type"))
            dbConnector = module.db_connector.DbConnector(**keys)
            dbConnector.connect()
            query_id = dbConnector.execute(query)
            queries_ids_info.append((rule_implementation["id"], query_id))

    array_results = []
    for rule_implementation_id, query_id in queries_ids_info:
        result = dbConnector.get_results(query_id)
        array_results.append({"rule_implementation_id": rule_implementation_id,
                              "date": datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'),
                              "result": result})

    path_save_results = constants.SAVE_RESULTS + \
    constants.NAME_FILE_TO_UPLOAD + constants.CSV_EXTENSION

    writeDictToCSV(path_save_results, constants.CSV_COLUMNS, array_results)
    return send_data_to_dq_results(path_save_results)
