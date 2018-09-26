from api.v1.exceptions.invalid_usage import InvalidUsage
from sqlparse.sql import Statement, Identifier
import sqlparse


class CustomValidation(object):


    @staticmethod
    def check_query(custom_validation_param):
        sql_tokens = sqlparse.parse(custom_validation_param["query_validation"])[0]

        if Statement(sql_tokens).get_type() != "SELECT" or Identifier(sql_tokens).is_wildcard():
            raise InvalidUsage('Not valid query', status_code=400)
