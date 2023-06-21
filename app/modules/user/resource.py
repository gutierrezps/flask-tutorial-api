from http import HTTPStatus
from time import time

import click
import jwt
from flask import Blueprint, current_app, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.globals import db, swag

from .model import User, UserSchema

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@swag.validate('UserRegistration')
def register():
    """Register a new user
    ---
    tags:
      - User/Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserRegistration
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: User's name
              minLength: 4
              maxLength: 20
            password:
              type: string
              description: User's password
              minLength: 4
              maxLength: 64
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: number
            username:
              type: string
      400:
        description: Invalid values or username already exists
    """
    username = request.json['username']

    user = User(
        username=username,
        password=generate_password_hash(request.json['password']))

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return {
                'error': f'username "{username}" already exists'
            }, HTTPStatus.BAD_REQUEST

    return UserSchema().dump(user), HTTPStatus.CREATED


@bp.route('/login', methods=['POST'])
@swag.validate('UserLogin')
def login():
    """User login
    ---
    tags:
      - User/Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserLogin
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: User's name
              maxLength: 20
            password:
              type: string
              description: User's password
              maxLength: 64
    responses:
      200:
        description: User created successfully
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Authentication failed
    """
    username = request.json['username']
    password = request.json['password']
    user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

    if user is not None and check_password_hash(user.password, password):
        token_data = {
            'username': user.username,
            'exp': int(time()) + 3600,
            'nbf': int(time()) - 60
        }
        token = jwt.encode(
            token_data,
            current_app.config['SECRET_KEY'],
            algorithm=current_app.config['TOKEN_ALG'])

        return {'token': token}

    return {'error': 'authentication failed'}, HTTPStatus.UNAUTHORIZED


@bp.cli.command('reset-pwd')
@click.argument('username')
@click.password_option()
def reset_password(username: str, password: str):
    """Reset the password of an user"""
    user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
    if user is None:
        click.echo('User does not exist')
        return
    user.password = generate_password_hash(password)
    db.session.commit()
    click.echo(f'Password for user {username} was reset')
