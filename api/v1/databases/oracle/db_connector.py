# -*- coding: utf-8 -*-
import cx_Oracle

class DbConnector(object):

    def __init__(self, username=None, password=None, hostname=None,
        port=None, servicename=None):

        if username is not None and password is not None \
            and hostname is not None and port is not None \
            and servicename is not None:
            self.username = username
            self.password = password
            self.hostname = hostname
            self.port = port
            self.servicename = servicename
            self.db = None

    def connect(self):
        """ Connect to the database. """

        try:
            dsn_tns = cx_Oracle.makedsn(self.hostname, self.port, service_name=self.servicename)
            self.db = cx_Oracle.connect(self.username, str(self.password), dsn_tns)
        except cx_Oracle.DatabaseError as e:
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
        except cx_Oracle.DatabaseError:
            pass

    def execute(self, sql, bindvars=None, commit=False):
        """
        Execute whatever SQL statements are passed to the method;
        commit if specified. Do not specify fetchall() in here as
        the SQL statement may not be a select.
        bindvars is a dictionary of variables you pass to execute.
        """

        try:
            self.cursor.execute(sql, bindvars)
        except cx_Oracle.DatabaseError as e:
            # Log error as appropriate
            raise

        # Only commit if it-s necessary.
        if commit:
            self.db.commit()
