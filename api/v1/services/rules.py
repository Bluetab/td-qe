# -*- coding: utf-8 -*-
from api.app import app
from api.common import constants
from api.common.utils import get_accept_auth_header, auth_token
from api.model.entities.custom_validations_model import CustomValidationsModel
from glom import glom, OMIT
 
import requests

class Rules(object):


    @staticmethod
    def get_data_from_dq(path_url, business_concept_id=None, status=None):
        response = requests.get(app.config["SERVICE_TD_DQ"] +
                                path_url.format(id=business_concept_id, status=status),
                                headers=get_accept_auth_header(auth_token()))
        data = response.json()["data"]
        return data


    @staticmethod
    def parser_result_get_rules(data):
        return list(filter(None, data))


    @staticmethod
    def parser_result_get_ri(rule_implementation_raw):
        spec = { "rule_implementation_id": ("id"), 
                "system": ("system"),
                "table": lambda t: t['system_params']["table"] if t['system_params'].get("table", None) else OMIT,
                "column": lambda t: t['system_params']["column"] if t['system_params'].get("column", None) else OMIT,
                "type": ("type")}
        return glom(rule_implementation_raw, spec)


    @staticmethod
    def get_query_by_type(rule_implementation, rule):

        switcher = {
            constants.TYPE_INTEGER_VALUES_RANGE: Rules.__query_integer_values_range,
            constants.TYPE_MIN_VALUE: Rules.__query_min_value,
            constants.TYPE_MAX_VALUE: Rules.__query_max_value,
            constants.TYPE_DATES_RANGE: Rules.__query_dates_range,
            constants.TYPE_MIN_DATE: Rules.__query_min_date,
            constants.TYPE_MAX_DATE: Rules.__query_max_date,
            constants.TYPE_MIN_TEXT: Rules.__query_min_text,
            constants.TYPE_MAX_TEXT: Rules.__query_max_text,
            constants.TYPE_MANDATORY_FIELD: Rules.__query_mandatory_field,
            constants.TYPE_CUSTOM: Rules.__query_custom_validation
        }


        return switcher.get(
            rule_implementation["type"],
            rule_implementation["type"])(rule_implementation, rule)


    @staticmethod
    def __query_integer_values_range(rule_implementation, rule):
        return constants.QUERY_INTEGER_VALUES_RANGE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_VALUE=rule["type_params"]["min_value"],
            MAX_VALUE=rule["type_params"]["max_value"])

    @staticmethod
    def __query_min_value(rule_implementation, rule):
        return constants.QUERY_MIN_VALUE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_VALUE=rule["type_params"]["min_value"])


    @staticmethod
    def __query_max_value(rule_implementation, rule):
        return constants.QUERY_MAX_VALUE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MAX_VALUE=rule["type_params"]["max_value"])


    @staticmethod
    def __query_dates_range(rule_implementation, rule):
        return constants.QUERY_DATES_RANGE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_DATE=rule["type_params"]["min_date"],
            MAX_DATE=rule["type_params"]["max_date"])


    @staticmethod
    def __query_min_date(rule_implementation, rule):
        return constants.QUERY_MIN_VALUE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_DATE=rule["type_params"]["min_date"])


    @staticmethod
    def __query_max_date(rule_implementation, rule):
        return constants.QUERY_MAX_VALUE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MAX_DATE=rule["type_params"]["max_date"])


    @staticmethod
    def __query_min_text(rule_implementation, rule):
        return constants.QUERY_MIN_TEXT.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_TEXT=rule["type_params"]["num_characters"])


    @staticmethod
    def __query_max_text(rule_implementation, rule):
        return constants.QUERY_MAX_TEXT.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MAX_TEXT=rule["type_params"]["num_characters"])


    @staticmethod
    def __query_mandatory_field(rule_implementation, rule):
        return constants.QUERY_MANDATORY_FIELD.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"])


    @staticmethod
    def __query_custom_validation(rule_implementation=None, rule=None):
        query_execute = CustomValidationsModel.find_by_rule_implementation_id(
            rule_implementation["rule_implementation_id"]
            ).to_dict()["query_validation"]
        return query_execute


