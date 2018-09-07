from api.common.utils import send_data_to_dq_results, writeDictToCSV, abort
from api.common import constants
from api.v1.services.rules import Rules
from flask import Blueprint, request
from api.common.auth import auth
from api.common import vault
import importlib
import datetime


rules = Blueprint('rules', __name__)


@rules.route('/engine/execute', methods=['POST'])
@auth.login_required
def all_rules():

    data = Rules.get_data_from_dq(constants.GET_QUALITY_CONTROLS)
    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


@rules.route('/engine/<int:business_concept_id>/execute', methods=['POST'])
@auth.login_required
def rules_by_id(business_concept_id):

    data = Rules.get_data_from_dq(constants.GET_QUALITY_CONTROLS_BY_BUSINESS_CONCEPT,
                                  business_concept_id)

    status_code = execute_rules_quality(data)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204


def execute_rules_quality(data):

    quality_controls = Rules.parser_result_get_qc(data)

    queries_ids_info = []
    for quality_control in quality_controls:
        quality_rules = quality_control["quality_rules"]
        for quality_rule_raw in quality_rules:
            quality_rule = Rules.parser_result_get_qr(quality_rule_raw)
            keys = vault.get_data_from_vault(constants.PATH_VAULT_SOURCES +
                                             quality_rule["system"])

            if keys != None:
                query = Rules.get_query_by_type(quality_rule, quality_control["type_params"])
                module = importlib.import_module(constants.API_DATABASE_PATH +
                                                 keys.pop("connection_type"))
                dbConnector = module.db_connector.DbConnector(**keys)
                dbConnector.connect()
                query_id = dbConnector.execute(query)
                queries_ids_info.append((quality_rule, query_id,
                                         quality_control["name"],
                                         quality_control["business_concept_id"]))


    array_results = []
    for quality_rule, query_id, quality_control_name, business_concept_id in queries_ids_info:
        result = dbConnector.get_results(query_id)
        array_results.append({"business_concept_id": business_concept_id,
                              "quality_control_name": quality_control_name,
                              "system": quality_rule["system"],
                              "group": quality_rule["table"],
                              "structure_name": quality_rule["table"],
                              "field_name": quality_rule["column"],
                              "date": datetime.date.today().strftime('%Y-%m-%d'),
                              "result": result})

    path_save_results = constants.SAVE_RESULTS + \
    constants.NAME_FILE_TO_UPLOAD + constants.CSV_EXTENSION

    writeDictToCSV(path_save_results, constants.CSV_COLUMNS, array_results)
    return send_data_to_dq_results(path_save_results)
