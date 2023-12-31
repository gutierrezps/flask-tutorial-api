import json
from http import HTTPStatus

from flasgger import Swagger
from flask import Response
from flask_httpauth import HTTPTokenAuth
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

db = SQLAlchemy()

migrate = Migrate()

ma = Marshmallow()


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 400 Bad Request
    response in case validation fails and returns the error
    """
    abort(Response(
        json.dumps({'error': f"{ err.relative_path[0] }: { err.message }"}),
        status=HTTPStatus.BAD_REQUEST))


swag = Swagger(validation_error_handler=validation_error_inform_error)


auth = HTTPTokenAuth(scheme='Bearer')
