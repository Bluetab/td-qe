from api.app import app
import hvac

def get_data_from_vault(path):

    client = hvac.Client(url=app.config["VAULT_HOST"])
    if client.is_sealed():
        client.unseal(app.config["VAULT_UNSEAL_KEY"])
    client.token = app.config["VAULT_TOKEN"]
    vault_data = client.read(path)
    client.logout()
    return vault_data["data"]["data"] if vault_data else None
