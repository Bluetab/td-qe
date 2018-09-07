from api.common.utils import send_data_to_dq_results, writeDictToCSV, abort
from api.common import constants
from api.v1.services.rules import Rules
from flask import Blueprint, request
from api.common.auth import auth
from api.common import vault
import importlib
import datetime


engine = Blueprint('engine', __name__)

@engine.route('/engine/execute', methods=['POST'])
@auth.login_required
def all_rules():

    data = Rules.get_data_from_dq(constants.GET_RULES, 
        status=constants.VALID_EXEC_STATUS)
    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


@engine.route('/engine/<int:business_concept_id>/execute', methods=['POST'])
@auth.login_required
def rules_by_id(business_concept_id):

    data = Rules.get_data_from_dq(
        constants.GET_RULES_BY_BUSINESS_CONCEPT,
        business_concept_id, 
        constants.VALID_EXEC_STATUS
    )

    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


def execute_rules_quality(data):

    rules = Rules.parser_result_get_rules(data)

    queries_ids_info = []
    for rule in rules:
        rule_implementations = rule["rule_implementations"]
        for rule_implementation_raw in rule_implementations:
            rule_implementation = Rules.parser_result_get_ri(rule_implementation_raw)
            keys = vault.get_data_from_vault(constants.PATH_VAULT_SOURCES +
                                             rule_implementation["system"])

            if keys != None:
                query = Rules.get_query_by_type(rule_implementation, rule)
                module = importlib.import_module(constants.API_DATABASE_PATH +
                                                 keys.pop("connection_type"))
                dbConnector = module.db_connector.DbConnector(**keys)
                dbConnector.connect()
                query_id = dbConnector.execute(query)
                queries_ids_info.append((rule_implementation, query_id,
                                         rule["name"],
                                         rule["business_concept_id"]))


    array_results = []
    for rule_implementation, query_id, rule_name, business_concept_id in queries_ids_info:
        result = dbConnector.get_results(query_id)
        array_results.append({"business_concept_id": business_concept_id,
                              "rule_name": rule_name,
                              "system": rule_implementation["system"],
                              "group": rule_implementation["table"],
                              "structure_name": rule_implementation["table"],
                              "field_name": rule_implementation["column"],
                              "date": datetime.date.today().strftime('%Y-%m-%d'),
                              "result": result})

    path_save_results = constants.SAVE_RESULTS + \
    constants.NAME_FILE_TO_UPLOAD + constants.CSV_EXTENSION

    writeDictToCSV(path_save_results, constants.CSV_COLUMNS, array_results)
    return send_data_to_dq_results(path_save_results)
