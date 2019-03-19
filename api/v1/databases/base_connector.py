from api.model.entities.custom_validations_model import CustomValidationsModel
from api.v1.databases.common import queries
from abc import ABCMeta, abstractmethod
from api.common import constants


class BaseConnector:

    def __init__(self,  *args, **kwargs):
        pass


    def execute_by_type(self, rule_implementation):
        switcher = {
            constants.TYPE_INTEGER_VALUES_RANGE: self._query_integer_values_range,
            constants.TYPE_MIN_VALUE: self._query_min_value,
            constants.TYPE_MAX_VALUE: self._query_max_value,
            constants.TYPE_DATES_RANGE: self._query_dates_range,
            constants.TYPE_MIN_DATE: self._query_min_date,
            constants.TYPE_MAX_DATE: self._query_max_date,
            constants.TYPE_MIN_TEXT: self._query_min_text,
            constants.TYPE_MAX_TEXT: self._query_max_text,
            constants.TYPE_MANDATORY_FIELD: self._query_mandatory_field,
            constants.TYPE_CUSTOM: self._query_custom_validation
        }

        rule = rule_implementation["rule"]
        type = rule["rule_type"]["name"]
        function_to_call = switcher.get(type, None)
        return self.__proccess_to_execute(function_to_call, rule_implementation, rule) if function_to_call else None


    def __proccess_to_execute(self, function_to_call, rule_implementation, rule):
        query_execute = function_to_call(rule_implementation, rule)
        self.connect()
        query_id = self.execute(query_execute)
        self.disconnect()
        return query_id


    def get_table_name(self, rule_implementation):
        return rule_implementation["table"]


    def get_column_name(self, rule_implementation):
        return rule_implementation["column"]


    def _query_integer_values_range(self, rule_implementation, rule):
        return queries.QUERY_INTEGER_VALUES_RANGE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MIN_VALUE=rule["type_params"]["min_value"],
            MAX_VALUE=rule["type_params"]["max_value"])


    def _query_min_value(self, rule_implementation, rule):
        return queries.QUERY_MIN_VALUE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MIN_VALUE=rule["type_params"]["min_value"])


    def _query_max_value(self, rule_implementation, rule):
        return queries.QUERY_MAX_VALUE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MAX_VALUE=rule["type_params"]["max_value"])


    def _query_dates_range(self, rule_implementation, rule):
        return queries.QUERY_DATES_RANGE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MIN_DATE=rule["type_params"]["min_date"],
            MAX_DATE=rule["type_params"]["max_date"])


    def _query_min_date(self, rule_implementation, rule):
        return queries.QUERY_MIN_VALUE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MIN_DATE=rule["type_params"]["min_date"])


    def _query_max_date(self, rule_implementation, rule):
        return queries.QUERY_MAX_VALUE.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MAX_DATE=rule["type_params"]["max_date"])


    def _query_min_text(self, rule_implementation, rule):
        return queries.QUERY_MIN_TEXT.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MIN_TEXT=rule["type_params"]["num_characters"])


    def _query_max_text(self, rule_implementation, rule):
        return queries.QUERY_MAX_TEXT.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation),
            MAX_TEXT=rule["type_params"]["num_characters"])


    def _query_mandatory_field(self, rule_implementation, rule):
        return queries.QUERY_MANDATORY_FIELD.format(
            TABLE=self.get_table_name(rule_implementation),
            COLUMN=self.get_column_name(rule_implementation))


    def _query_custom_validation(self, rule_implementation=None, rule=None):
        query_execute = CustomValidationsModel.find_by_implementation_key(
            rule_implementation["implementation_key"]
            ).to_dict()["query_validation"]
        return query_execute
