from flask import Flask, make_response, jsonify
from api.model.base_model import db
from flask_cors import CORS
import os

environ = os.getenv("APP_ENV", "Development") if \
    os.getenv("APP_ENV", "Development") in ["Development", "Production", "Testing"] \
    else "Development"

app = Flask(__name__)
CORS(app)
app.config.from_object('api.settings.config.{}Config'.format(environ))

db.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from api.v1.engine import engine
from api.v1.custom_validations import custom_validations

API_V1 = '/api'

app.register_blueprint(engine, url_prefix=API_V1)
app.register_blueprint(custom_validations, url_prefix=API_V1)
