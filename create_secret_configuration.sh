#!/bin/bash

sed -i -e "s/SECRET_KEY = .*/SECRET_KEY = \"$GUARDIAN_SECRET_KEY\"/g" ./api/settings/config.py
sed -i -e "s/VAULT_TOKEN = .*/VAULT_TOKEN: \"$VAULT_TOKEN\"/g" ./api/settings/config.py
sed -i -e "s/VAULT_HOST = .*/VAULT_HOST = \"$VAULT_HOST\"/g" ./api/settings/config.py
sed -i -e "s/API_USERNAME = .*/API_USERNAME = \"$API_USERNAME\"/g" ./api/settings/config.py
sed -i -e "s/API_PASSWORD = .*/API_PASSWORD = \"$API_PASSWORD\"/g" ./api/settings/config.py
