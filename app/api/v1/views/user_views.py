""""The User route endpints"""

import os
import datetime

import jwt
from flask import request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v1.utils import validators
from app.api.v1.models.models import User
from app.api.v1 import version1

KEY = os.getenv('SECRET_KEY')

@version1.route("/auth/signup", methods=['POST'])
def user_sign_up():
    """
    The user sign up route
    """
    try:
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_pass = data['confirm_password']

    except KeyError:
        abort(make_response(jsonify({
            'error':'Check your json keys', 'status': 400}), 400))


    validators.check_for_whitespace(data)

    validators.check_password(password, confirm_pass)
    email = validators.validate_email(email)

    user = User(firstname=firstname,
                username=username,
                lastname=lastname,
                email=email,
                password=password)

    user.save_user()
    return jsonify({"status":201, "data":"Registered successfully!"}), 201


@version1.route("/auth/login", methods=['POST'])
def user_login():
    """
    The user login route
    """
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            ' error': "Check your json keys. Should be username & password"}), 400))

    validators.check_for_whitespace(data)
    validators.verify_if_admin(username)

    wrong_username = validators.query_db_wrong_username(username, password)
    if wrong_username:
        return jsonify({"status": 400, "error":"The username is incorrect"}), 400

    wrong_pass = validators.query_db_wrong_password(username, password)
    if wrong_pass:
        abort(make_response(jsonify({
            'status':400, 'error':'Wrong password'}), 400))

    user = User.query_users(username, password)

    if not user:
        return jsonify({"status": 400, "data":"Please Register first"}), 400

    token = jwt.encode({"username":username}, KEY, algorithm='HS256')
    return jsonify({
        "status": 200,
        "token":token.decode('UTF-8'),
        "message": "Logged in successfully"}), 200
