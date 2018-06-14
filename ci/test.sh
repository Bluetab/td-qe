#! /bin/bash

cp -R /code /working_code
cd /working_code
sed -i -e "s/sudo\s//g" ./scripts/*

rm -rf /working_code/venv || exit 1
virtualenv -p python3.6 /working_code/venv
source /working_code/venv/bin/activate

echo "Starting tests"
python setup.py test || exit 1

# export APP_ENV=Testing
# echo "Starting behave"
# behave || exit 1

echo "Test step finish successfully"
