# -*- coding: utf-8 -*-
from api.common.utils import get_accept_auth_header, auth_token
from api.common import constants
from glom import glom, OMIT
from api.app import app
import requests

class Rules(object):


    @staticmethod
    def get_data_from_dq(path_url, business_concept_id=None):
        response = requests.get(app.config["SERVICE_TD_DQ"] +
                                path_url.format(id=business_concept_id),
                                headers=get_accept_auth_header(auth_token()))
        data = response.json()["data"]
        return data


    @staticmethod
    def parser_result_get_qc(data):
        spec = [{'quality_rules': lambda t: t['rule_implementations'] if t['status'] == 'implemented' else OMIT,
                'type_params': lambda t: t['type_params'] if t['status'] == 'implemented' else OMIT,
                'name': lambda t: t['name'] if t['status'] == 'implemented' else OMIT,
                'business_concept_id': lambda t: t['business_concept_id'] if t['status'] == 'implemented' else OMIT}]
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
            constants.TYPE_MIN_VALUE: Rules.__query_min_value,
            constants.TYPE_MAX_VALUE: Rules.__query_max_value,
            constants.TYPE_DATES_RANGE: Rules.__query_dates_range,
            constants.TYPE_MIN_DATE: Rules.__query_min_date,
            constants.TYPE_MAX_DATE: Rules.__query_max_date,
            constants.TYPE_MIN_TEXT: Rules.__query_min_text,
            constants.TYPE_MAX_TEXT: Rules.__query_max_text,
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
    def __query_min_value(quality_rule, type_params):
        return constants.QUERY_MIN_VALUE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MIN_VALUE=type_params["min_value"])


    @staticmethod
    def __query_max_value(quality_rule, type_params):
        return constants.QUERY_MAX_VALUE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MAX_VALUE=type_params["max_value"])


    @staticmethod
    def __query_dates_range(quality_rule, type_params):
        return constants.QUERY_DATES_RANGE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MIN_DATE=type_params["min_date"],
            MAX_DATE=type_params["max_date"])


    @staticmethod
    def __query_min_date(quality_rule, type_params):
        return constants.QUERY_MIN_VALUE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MIN_DATE=type_params["min_date"])


    @staticmethod
    def __query_max_date(quality_rule, type_params):
        return constants.QUERY_MAX_VALUE.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MAX_DATE=type_params["max_date"])


    @staticmethod
    def __query_min_text(quality_rule, type_params):
        return constants.QUERY_MIN_TEXT.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MIN_TEXT=type_params["num_characters"])


    @staticmethod
    def __query_max_text(quality_rule, type_params):
        return constants.QUERY_MAX_TEXT.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"],
            MAX_TEXT=type_params["num_characters"])


    @staticmethod
    def __query_mandatory_field(quality_rule, type_params):
        return constants.QUERY_MANDATORY_FIELD.format(
            TABLE=quality_rule["table"],
            COLUMN=quality_rule["column"])
