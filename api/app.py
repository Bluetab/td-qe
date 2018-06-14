from flask import Flask, make_response, jsonify
from flask_cors import CORS
import os

environ = os.getenv("APP_ENV", "Development") if \
    os.getenv("APP_ENV", "Development") in ["Development", "Production", "Testing"] \
    else "Development"

app = Flask(__name__)
CORS(app)
app.config.from_object('api.settings.config.{}Config'.format(environ))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

from api.v1.rules import rules

API_V1 = '/api'

app.register_blueprint(rules, url_prefix=API_V1)
