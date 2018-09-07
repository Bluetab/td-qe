# -*- coding: utf-8 -*-
import psycopg2

class DbConnector(object):

    def __init__(self, username=None, password=None, hostname=None,
        port=None, database=None):

        if username is not None and password is not None \
            and hostname is not None and port is not None \
            and database is not None:
            self.username = username
            self.password = password
            self.hostname = hostname
            self.port = port
            self.database = database
            self.db = None

    def connect(self):
        """ Connect to the database. """

        try:
            self.db = psycopg2.connect(dbname=self.database, port=self.port, host=self.hostname, user=self.username, password=self.password)
        except psycopg2.Error as e:
            # Log error as appropriate
            raise

        # If the database connection succeeded create the cursor
        # we-re going to use.
        self.cursor = self.db.cursor()

    def disconnect(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist, ignore the exception.
        """

        try:
            self.cursor.close()
            self.db.close()
        except psycopg2.Error:
            pass

    def execute(self, sql, bindvars=None, commit=False):
        """
        Execute whatever SQL statements are passed to the method;
        commit if specified. Do not specify fetchall() in here as
        the SQL statement may not be a select.
        bindvars is a dictionary of variables you pass to execute.
        """

        try:
            self.cursor.execute(sql, vars=bindvars)
            percentage = self.cursor.fetchone()[0]
        except psycopg2.Error as e:
            # Log error as appropriate
            raise

        # Only commit if it-s necessary.
        if commit:
            self.db.commit()

        return percentage

    def get_results(self, query_id):
        return query_id
