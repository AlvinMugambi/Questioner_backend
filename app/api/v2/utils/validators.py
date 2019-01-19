"""The validator functions that validate user data"""
import os
import re
from functools import wraps
from datetime import datetime

import jwt
from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash

# local imports
from app.api.v2.models.database import select_from_db

key = os.getenv("SECRET_KEY")

def check_password(password, confirmed_password):
    """
    The checker function that checks if password meets required parameters
    """
        # check if password meets required length
    if len(password) < 6 or len(password) > 12:
        abort(make_response(jsonify(
            status=400,
            error="Password should not be less than 6 characters or exceed 12"), 400))

    # check if password contains at least an alphabet(a-z)
    if not re.search("[a-z]", password):
        abort(make_response(jsonify(
            status=400,
            error="Password should contain a letter between a-z"), 400))

    # check if password contains at least an upper case letter
    if not re.search("[A-Z]", password):
        abort(make_response(jsonify(
            status=400,
            error="Password should contain a capital letter"), 400))

    # check if password contains at least a number(0-9)
    if not re.search("[0-9]", password):
        abort(make_response(jsonify(
            status=400,
            error="Password should contain a number(0-9)"), 400))

    # Checks if passwords provided by the users match
    if password != confirmed_password:
        abort(make_response(jsonify(
            status=400,
            error="Passwords don't match!"), 400))

    # If they match..
    hashed_password = generate_password_hash(password, method='sha256')

    return hashed_password


def validate_email(email):
    """
    The checker function for validating an Email
    if the email is a valid email and if it is already in use
    """
    try:
        user, domain = str(email).split("@")
        if not re.match("^[A-Za-z]*$", user):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Invalid Email"}), 400))
    except ValueError:
        abort(make_response(jsonify(
            status=400,
            error="Invalid Email"), 400))
    if not user or not domain:
        abort(make_response(jsonify(error="Invalid Email"), 400))

    # Check that domain is valid
    try:
        dom_1, dom_2 = domain.split(".")
        if not re.match("^[A-Za-z]*$", dom_1):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Invalid Email"}), 400))
        if not re.match("^[A-Za-z]*$", dom_2):
            abort(make_response(jsonify({
                "status": 400, "Error":  "Invalid Email"}), 400))
    except ValueError:
        abort(make_response(jsonify(
            status=400,
            error="Invalid Email"), 400))
    if not dom_1 or not dom_2:
        abort(make_response(jsonify(
            status=400,
            error="Invalid Email"), 400))

    return email

def check_for_whitespace(data):
    """
    Check for whitespace only in input data
    """
    for keys, value in data.items():
        if not value.strip():
            abort(make_response(jsonify({
                'status': 400,
                'error':'{} field cannot be left blank'.format(keys)}), 400))

    return True

def check_if_string(data):
    for key, value in data.items():
        if key in ['firstname', 'lastname', 'username']:
            if not value.isalpha():
                abort(make_response(jsonify({
                    "status": 400,
                    "Error":  "Make sure you only use letters in your {}".format(key)}), 400))


def check_phone_number(phone):
    if not re.match('^[0-9]*$', phone):
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Phone number should be integers only"}), 400))

    if len(phone) < 10 or len(phone) > 10:
        abort(make_response(jsonify({
            "status": 400,
            "Error":  "Phone number should be 10 digits."}), 400))


def check_date(date):
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/([12][0-9]{3})$", date):
        abort(make_response(jsonify({
            "status": 400, "Error":  "Invalid date format. Should be DD/MM/YYYY"}), 400))

    date_format = "%d/%m/%Y"
    # create datetime objects from the strings
    strpdate = datetime.strptime(date, date_format)
    now = datetime.now()

    if strpdate < now:
        abort(make_response(jsonify({
            "status": 400, "Error":  "Date should be in the future"}), 400))

    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    format_date = date[0:2]+ " " + months[int(date[3:5]) -1] + " " + date[6:]
    return format_date


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
                status=400,
                error="Error. '{}' '{}' \
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
            query = """
            SELECT username FROM users
            WHERE users.username = '{}'""".format(data['username'])

            current_user = select_from_db(query)

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
