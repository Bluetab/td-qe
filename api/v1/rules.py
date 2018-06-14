from api.common.utils import send_data_to_dq_results, writeDictToCSV, abort
from api.common.constants import (PATH_VAULT_SOURCES, NAME_FILE_TO_UPLOAD,
                                  API_DATABASE_PATH, SAVE_RESULTS,
                                  CSV_EXTENSION)
from api.v1.services.rules import Rules
from flask import Blueprint, request
from api.common.auth import auth
from api.common import vault
import importlib
import datetime


rules = Blueprint('rules', __name__)

@rules.route('/rules/<int:business_concept_id>/execute', methods=['POST'])
@auth.login_required
def execute(business_concept_id):

    data = Rules.get_data_from_dq(business_concept_id)
    quality_controls = Rules.parser_result_get_qc(data)

    queries_ids_info = []
    for quality_control in quality_controls:
        quality_rules = quality_control["quality_rules"]
        for quality_rule_raw in quality_rules:
            quality_rule = Rules.parser_result_get_qr(quality_rule_raw)
            keys = vault.get_data_from_vault(PATH_VAULT_SOURCES + quality_rule["system"])
            query = Rules.get_query_by_type(quality_rule, quality_control["type_params"])
            module = importlib.import_module(API_DATABASE_PATH + keys.pop("connection_type"))
            dbConnector = module.db_connector.DbConnector(**keys)
            dbConnector.connect()
            query_id = dbConnector.execute(query)
            queries_ids_info.append((quality_rule, query_id, quality_control["name"]))

    array_results = []
    csv_columns = ['business_concept_id','quality_control_name','system',
                   'group', 'structure_name', 'field_name',
                   'date', 'result']

    for quality_rule, query_id, quality_control_name in queries_ids_info:
        result = dbConnector.get_results(query_id)
        array_results.append({"business_concept_id": business_concept_id,
                              "quality_control_name": quality_control_name,
                              "system": quality_rule["system"],
                              "group": quality_rule["table"],
                              "structure_name": quality_rule["table"],
                              "field_name": quality_rule["column"],
                              "date": datetime.date.today().strftime('%Y-%m-%d'),
                              "result": result})

    path_save_results = SAVE_RESULTS + NAME_FILE_TO_UPLOAD + CSV_EXTENSION
    writeDictToCSV(path_save_results, csv_columns, array_results)
    status_code = send_data_to_dq_results(path_save_results)
    if status_code != 200:
        return abort(422, {'message': "unprocessable entity"})
    return "", 204
