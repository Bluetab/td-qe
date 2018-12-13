from api.v1.exceptions.invalid_usage import InvalidUsage
from api.app import app
import hvac

def get_data_from_vault(path):

    client = hvac.Client(url=app.config["VAULT_HOST"])
    if client.is_sealed():
        raise InvalidUsage('Error getting credentials. Check Vault', status_code=400)
    client.token = app.config["VAULT_TOKEN"]
    vault_data = client.read(path)
    if not vault_data:
        print("No data found in vault path {path}".format(path=path))
    client.logout()
    return vault_data["data"]["data"] if vault_data else None
