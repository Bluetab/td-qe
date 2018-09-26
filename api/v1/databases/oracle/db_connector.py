# -*- coding: utf-8 -*-
from api.v1.databases.base_connector import BaseConnector
from api.v1.databases.oracle import queries
import cx_Oracle

class DbConnector(BaseConnector):

    def __init__(self, username=None, password=None, hostname=None,
        port=None, servicename=None):

        if username is not None and password is not None \
            and hostname is not None and port is not None \
            and servicename is not None:
            self.username = username
            self.password = password
            self.db = None
            self.__dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=servicename)


    def connect(self):

        try:
            self.db = cx_Oracle.connect(self.username, str(self.password), self.__dsn_tns)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise

        self.cursor = self.db.cursor()


    def disconnect(self):

        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError:
            pass


    def execute(self, sql, bindvars=None, commit=False):

        try:
            self.cursor.execute(sql)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise

        # Only commit if it-s necessary.
        if commit:
            self.db.commit()

        return self.cursor.fetchone()[0]


    def _query_integer_values_range(self, rule_implementation, rule):
        return queries.QUERY_INTEGER_VALUES_RANGE.format(
            TABLE=rule_implementation["table"],
            COLUMN=rule_implementation["column"],
            MIN_VALUE=rule["type_params"]["min_value"],
            MAX_VALUE=rule["type_params"]["max_value"])


    def get_results(self, query_id):
        return query_id
