# -*- coding: utf-8 -*-
import pymssql

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
            self.conn = None

    def connect(self):
        """ Connect to the database. """

        self.conn = pymssql.connect(server=self.hostname, user=self.username, port=self.port, password=self.password, database=self.database)
        self.cursor = self.conn.cursor()


    def disconnect(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist, ignore the exception.
        """

        self.cursor.close()
        self.conn.close()


    def execute(self, sql, bindvars=None, commit=False):
        """
        Execute whatever SQL statements are passed to the method;
        commit if specified. Do not specify fetchall() in here as
        the SQL statement may not be a select.
        bindvars is a dictionary of variables you pass to execute.
        """

        self.cursor.execute(sql)

        # Only commit if it-s necessary.
        if commit:
            self.conn.commit()
