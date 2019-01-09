# -*- coding: utf-8 -*-
from api.common.utils import get_accept_auth_header, auth_token
from api.common.utils import send_data_to_dq_results, writeDictToCSV
from api.v1.support.support import Support
from api.common import constants
from glom import glom, OMIT
from flask import request
from api.app import app
import requests
import datetime


class Engine(object):


    @staticmethod
    def get_data_from_dq(path_url, business_concept_id=None, status=None, rule_tags=None):
        rule_tags = constants.PARAM_RULE_TAGS.format(rule_tags=','.join(rule_tags)) if rule_tags else ""
        response = requests.get(app.config["SERVICE_TD_DQ"] +
                                path_url.format(
                                    id=business_concept_id, status=status) + rule_tags,
                                headers=get_accept_auth_header(auth_token()))
        data = response.json()["data"]
        print("Data from DQ: " + str(len(data)))
        return data


    @staticmethod
    def parse_rule_implementations(data_raw):
        spec = [{"implementation_key": ("implementation_key"),
                "system": ("system"),
                "group":  lambda t: t['system_params']["group"]  if t['system_params'].get("group", None)  else OMIT,
                "table":  lambda t: t['system_params']["table"]  if t['system_params'].get("table", None)  else OMIT,
                "column": lambda t: t['system_params']["column"] if t['system_params'].get("column", None) else OMIT,
                "rule": ("rule")}]
        return glom(data_raw, spec)


    @staticmethod
    def execute_rules_quality(data_raw):
        rule_implementations = Engine.parse_rule_implementations(data_raw)
        print("Rule Implementations to proccess: " + str(len(rule_implementations)))

        connectors_object = Support.set_connector_object(rule_implementations)
        print("Connectors Object: " + str(connectors_object))

        queries_ids_info = []
        for rule_implementation in rule_implementations:
            if rule_implementation["system"] in connectors_object:
                dbConnector = connectors_object[rule_implementation["system"]]
                query_id = dbConnector.execute_by_type(rule_implementation)
                queries_ids_info.append((rule_implementation["implementation_key"], query_id))

        print("Query Results: " + str(len(queries_ids_info)))

        array_results = []
        for implementation_key, query_id in queries_ids_info:
            result = dbConnector.get_results(query_id)
            array_results.append({"implementation_key": implementation_key,
                                  "date": datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'),
                                  "result": result})

        path_save_results = constants.SAVE_RESULTS + \
        constants.NAME_FILE_TO_UPLOAD + constants.CSV_EXTENSION

        writeDictToCSV(path_save_results, constants.CSV_COLUMNS, array_results)
        return send_data_to_dq_results(path_save_results)
