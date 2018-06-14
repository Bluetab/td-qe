# -*- coding: utf-8 -*-
from api.common.utils import get_accept_auth_header, auth_token
from api.common import constants
from glom import glom, OMIT
from api.app import app
import requests

class Rules(object):


    @staticmethod
    def get_data_from_dq(business_concept_id):
        response = requests.get(app.config["SERVICE_TD_DQ"] +
                                constants.GET_QUALITY_RULES.format(id=business_concept_id),
                                headers=get_accept_auth_header(auth_token()))
        data = response.json()["data"]
        return data


    @staticmethod
    def parser_result_get_qc(data):
        spec = [{'quality_rules': lambda t: t['quality_rules'] if t['status'] == 'implemented' else OMIT,
                'type_params': lambda t: t['type_params'] if t['status'] == 'implemented' else OMIT,
                'name': lambda t: t['name'] if t['status'] == 'implemented' else OMIT}]
        return list(filter(None, glom(data, spec)))


    @staticmethod
    def parser_result_get_qr(quality_rule_raw):
        spec = {"system": ("system"),
                "table": ("system_params.table"),
                "column": ("system_params.column"),
                "type": ("type")}
        return glom(quality_rule_raw, spec)


    @staticmethod
    def get_query_by_type(quality_rule, type_params):

        switcher = {
            constants.TYPE_INTEGER_VALUES_RANGE: Rules.__query_integer_values_range,
            constants.TYPE_MANDATORY_FIELD: Rules.__query_mandatory_field
        }

        return switcher.get(
            quality_rule["type"],
            quality_rule["type"])(quality_rule, type_params)


    @staticmethod
    def __query_integer_values_range(quality_rule, type_params):
        return constants.QUERY_INTEGER_VALUES_RANGE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MIN_VALUE=type_params["min_value"],
            MAX_VALUE=type_params["max_value"])


    @staticmethod
    def __query_mandatory_field(quality_rule, type_params):
        return constants.QUERY_MANDATORY_FIELD.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"])
