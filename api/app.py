from api.v1.exceptions.invalid_usage import InvalidUsage
from flask import Flask, make_response, jsonify
from api.settings.swagger_config import swagger_config
from api.model.base_model import db
from flask_migrate import Migrate
from flask_migrate import upgrade
from flasgger import Swagger
from flask_cors import CORS
import os

environ = os.getenv("APP_ENV", "Development") if \
    os.getenv("APP_ENV", "Development") in ["Development", "Production", "Testing"] \
    else "Development"

app = Flask(__name__)
CORS(app)
app.config.from_object('api.settings.config.{}Config'.format(environ))

app.config['SWAGGER'] = {
    'title': 'Quality Engine API',
    'uiversion': 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "TD-QE",
        "description": "TD-QE API",
        "version": "0.0.1"
    },
    "host": app.config['SWAGGER_HOST'],
    "schemes": ["http"],
    "securityDefinitions": {
        "bearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    },
    "security": [{ "bearerAuth": [] }]
}

swag = Swagger(app, template=swagger_template,
        config=swagger_config)


db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


from api.v1.engine import engine
from api.v1.custom_validations import custom_validations

API_V1 = '/api'

app.register_blueprint(engine, url_prefix=API_V1)
app.register_blueprint(custom_validations, url_prefix=API_V1)





@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
