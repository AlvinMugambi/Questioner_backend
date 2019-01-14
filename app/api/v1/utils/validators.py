"""The validator functions that validate user data"""
import os
import re
from functools import wraps

import jwt
from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash

# local imports
from app.api.v1.models.models import User, USERS

key = os.getenv("SECRET_KEY")


def check_password(password, confirmed_password):
    """
    The checker function that checks if password meets required parameters
    """
        # check if password meets required length
    if len(password) < 6 or len(password) > 12:
        abort(make_response(jsonify(
            error="Password should not be less than 6 characters or exceed 12"), 400))

    # check if password contains at least an alphabet(a-z)
    if not re.search("[a-z]", password):
        abort(make_response(jsonify(
            error="Password should contain a letter between a-z"), 400))

    # check if password contains at least an upper case letter
    if not re.search("[A-Z]", password):
        abort(make_response(jsonify(
            error="Password should contain a capital letter"), 400))

    # check if password contains at least a number(0-9)
    if not re.search("[0-9]", password):
        abort(make_response(jsonify(
            error="Password should contain a number(0-9)"), 400))

    # Checks if passwords provided by the users match
    if password != confirmed_password:
        abort(make_response(jsonify(
            error="Passwords don't match!"), 400))

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


def check_for_whitespace(data):
    for keys, value in data.items():
        if not value.strip():
            abort(make_response(jsonify({
                'status': 400,
                'error':'{} field cannot be left blank'.format(keys)}), 400))

    return True


def query_db_wrong_password(username, password):
    """
    Query db for a registered user but enters wrong password
    """
    wrong_pass = None
    for user in USERS:
        if user.username == username:
            if user.password != password:
                wrong_pass = True

    return wrong_pass


def query_db_wrong_username(username, password):
    """
    Query db for a registered user but enters wrong password
    """
    wrong_pass = None
    for user in USERS:
        if user.password == password:
            if user.username != username:
                wrong_pass = True

    return wrong_pass


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


def token_required(f):
    """The token required decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """The decrated function"""
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
    """
    Decode token to query for the logged in user username
    """
    token = request.headers['x-access-token']
    try:
        username = jwt.decode(token, key)
    except:
        return jsonify({"message":"Token is expired or invalid"}), 401

    return username
