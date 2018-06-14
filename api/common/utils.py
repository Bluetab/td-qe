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


def abort(status_code, body=None):
    return make_response(jsonify(body), status_code)


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


def checkparams(params, request):
    if not request.json:
        return "Error body json not found"
    for param in params:
        if param not in request.json:
            return "Error {} not found".format(param)
    return False


def checkonlyone(params, request):
    if not request.json:
        return "Error body json not found", None
    total = []
    for param in params:
        if param in request.json:
            total.append(param)
    if len(total) > 1:
        return "Error, multiple params founds: {}. \
                You can use only one".format(",".join(total)), None
    if len(total) == 0:
        return "Error, params {} not founds".format(" or ".join(params)), None
    return False, total[0]


def findInArgs(default, args):
    arg = ""
    value = ""
    for key, value in args.items():
        if key == default:
            arg = default
            value = value
    if arg == "":
        return "Error, '{}' not found in args".format(default), None
    return False, [arg, value]


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec
