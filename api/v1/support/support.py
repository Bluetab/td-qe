from api.common import constants
from functools import reduce
from api.common import vault
import importlib


class Support(object):


    @staticmethod
    def set_connector_object(rule_implementations):
        return reduce(
            lambda connectors_object, rule_implementation: Support.get_object_from_vault(
                connectors_object, rule_implementation["system"])
            if rule_implementation["system"] not in connectors_object
            else connectors_object, rule_implementations, {})


    @staticmethod
    def get_object_from_vault(connectors_object, system):
        params_system_vault = vault.get_data_from_vault(
            constants.PATH_VAULT_SOURCES + system)

        if params_system_vault != None:
            module = importlib.import_module(
                constants.API_DATABASE_PATH +
                params_system_vault.pop("connection_type"))
            dbConnector = module.db_connector.DbConnector(**params_system_vault)
            connectors_object.update({system : dbConnector})

        return connectors_object
