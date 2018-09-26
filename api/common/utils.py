from api.common.constants import (HEADERS_ACCEPT, HEADERS_CONTENT,
                                  SESSIONS, NAME_KEY_FILES_DQ,
                                  SEND_CSV_RESULTS)
from flask import make_response, jsonify
from api.app import app
import requests
import json
import csv


def auth_token():
    username = app.config["API_USERNAME"]
    password = app.config["API_PASSWORD"]
    data = {"user": {"user_name": username, "password": password}}
    r = requests.post(app.config["SERVICE_TD_AUTH"] + SESSIONS,
                      data=json.dumps(data), headers=HEADERS_CONTENT)
    token = r.json()['token']
    return token


def get_content_auth_header(token):
    HEADERS = HEADERS_CONTENT
    HEADERS.update(
        {'Authorization': 'Bearer {token}'.format(token=token)})
    return HEADERS


def get_content_accept_auth_header(token):
    HEADERS = HEADERS_CONTENT
    HEADERS.update(HEADERS_ACCEPT)
    HEADERS.update(
        {'Authorization': 'Bearer {token}'.format(token=token)})
    return HEADERS


def get_accept_auth_header(token):
    HEADERS = HEADERS_ACCEPT
    HEADERS.update(
        {'Authorization': 'Bearer {token}'.format(token=token)})
    return HEADERS


def get_auth_header(token):
    return {'Authorization': 'Bearer {token}'.format(token=token)}


def writeDictToCSV(csv_file, csv_columns, dict_data):

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=csv_columns, delimiter=';',
                                    quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError :
            print("I/O error({0})".format(csv_file))


def send_data_to_dq_results(name_file):

    tuple_files = [(NAME_KEY_FILES_DQ, open(name_file, 'rb'))]
    resp = requests.post(app.config["SERVICE_TD_DQ"] + SEND_CSV_RESULTS,
                         files=tuple_files, headers=get_auth_header(auth_token()))
    return resp.status_code


def get_auth_header(token):
    return {'Authorization': 'Bearer {token}'.format(token=token)}
