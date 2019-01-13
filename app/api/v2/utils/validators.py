"""The validator functions that validate user data"""
import os
import re
from functools import wraps

import jwt
from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash

# local imports
from app.api.v1.models.models import User, USERS
from app.api.v2.models.database import select_from_db

key = os.getenv("SECRET_KEY")

def check_password(password, confirmed_password):
    """
    The checker function that checks if password meets required parameters
    """
        # check if password meets required length
    if len(password) < 6 or len(password) > 12:
        abort(make_response(jsonify(error="Password should not be less than 6 characters or exceed 12"), 400))

    # check if password contains at least an alphabet(a-z)
    if not re.search("[a-z]", password):
        abort(make_response(jsonify(error="Password should contain a letter between a-z"), 400))

    # check if password contains at least an upper case letter
    if not re.search("[A-Z]", password):
        abort(make_response(jsonify(error="Password should contain a capital letter"), 400))

    # check if password contains at least a number(0-9)
    if not re.search("[0-9]", password):
        abort(make_response(jsonify(error="Password should contain a number(0-9)"), 400))

    # Checks if passwords provided by the users match
    if password != confirmed_password:
        abort(make_response(jsonify(error="Passwords don't match!"), 400))

    # If they match..
    hashed_password = generate_password_hash(password, method='sha256')

    return hashed_password


def validate_email(email):
    """
    The checker function for validating an Email
     check if the email is a valid email and if it is already in use
    """

    for user in USERS:
        if email == user.email:
            abort(make_response(jsonify(error="Email already taken!"), 400))
    try:
        user, domain = str(email).split("@")
    except ValueError:
        abort(make_response(jsonify(error="Invalid Email"), 400))
    if not user or not domain:
        abort(make_response(jsonify(error="Invalid Email"), 400))

    # Check that domain is valid
    try:
        dom_1, dom_2 = domain.split(".")
    except ValueError:
        abort(make_response(jsonify(error="Invalid Email"), 400))
    if not dom_1 or not dom_2:
        abort(make_response(jsonify(error="Invalid Email"), 400))

    return email

def verify_if_admin(username):
    """
    Verifies if the user is admin
    """
    admin = None
    for user in USERS:
        if username == 'iamtheadmin':
            user.is_admin = True
            admin = True
        admin = False
    return admin

def check_if_admin():
    """
    Checks if the user is an admin
    """
    username = decode_token()

    if username['username'] != "iamtheadmin":
        return False
    return True


def check_duplication(params, table_name):
    """
        Check if a user is already in db, abort if found
    """
    for key, value in params.items():
        query = """
        SELECT {} from {} WHERE {}.{} = '{}'
        """.format(key, table_name, table_name, key, value)
        duplicated = select_from_db(query)
        if duplicated:
            # Abort if duplicated
            abort(make_response(jsonify(
                message="Error. '{}' '{}' \
is already in use".format(key, value)), 400))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':"Token is missing"}), 401

        try:
            data = jwt.decode(token, key)
            current_user = None
            for user in USERS:
                if user.username == data['username']:
                    current_user = user

        except:
            return jsonify({'message':'Token is expired or invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def decode_token():
    token = request.headers['x-access-token']
    try:
        username = jwt.decode(token, key)
    except:
        return jsonify({"message":"Token is expired or invalid"}), 401

    return username