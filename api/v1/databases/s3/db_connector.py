# -*- coding: utf-8 -*-
from time import sleep
from glom import glom
import boto3


class DbConnector(object):

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None, bucket=None):

        if aws_access_key_id is not None and aws_secret_access_key is not None \
            and region_name is not None and bucket is not None:
            self.aws_access_key_id = aws_access_key_id
            self.aws_secret_access_key = aws_secret_access_key
            self.region_name = region_name
            self.bucket = bucket
            self.__session = None


    def connect(self):
        """ Connect to the database. """

        self.__session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )


    def disconnect(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist, ignore the exception.
        """
        self.__session = None


    def start_query_execution(self, query, bucket):

        query_id = self.__session.client(
            'athena').start_query_execution(
                QueryString=query, ResultConfiguration=
                {'OutputLocation': bucket})["QueryExecutionId"]

        return query_id


    def __get_query_execution(self, query_id):

        target = self.__session.client(
            'athena').get_query_execution(QueryExecutionId=query_id)

        return glom(target, spec = 'QueryExecution.Status.State')


    def get_query_results(self, query_id):

        while True:
            result_query = self.__get_query_execution(query_id)
            if result_query == "FAILED" or result_query == "SUCCEEDED":
                break
            else:
                sleep(0.05)

        response = result_query
        if result_query == "SUCCEEDED":
            response = self.__session.client(
                'athena').get_query_results(QueryExecutionId=query_id)

        return response
