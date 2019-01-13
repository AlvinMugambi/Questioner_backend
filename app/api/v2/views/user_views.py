import os
import jwt
from flask import request, jsonify, abort, make_response
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.utils import validators
from app.api.v2.models.models import User
from app.api.v2 import version2

KEY = os.getenv('SECRET_KEY')

@version2.route("/auth/signup", methods=['POST'])
def user_sign_up():
    try:
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        confirm_pass = request.get_json()['confirm_password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     'error': "Check your json keys"}), 400))

    validators.check_password(password, confirm_pass)
    email = validators.validate_email(email)

    validators.check_duplication({"username": username}, "users")
    validators.check_duplication({"email": email}, "users")

    user = User(username=username,
                email=email,
                password=password)

    user.save_user()
    return jsonify({"status":201, "data":"Registered successfully!"}), 201


@version2.route("/auth/login", methods=['POST'])
def user_login():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Check your json keys. Should be username & password"}), 400))
    try:
        user = User.get_user_by_username(username)
        if not user:
            return jsonify({"status": 400, "data":"Register first"}), 400

        user_id = user[0][0]
        username = user[0][1]
        email = user[0][2]
        hashed_password = user[0][3]

        password = User.check_if_password_in_db(hashed_password, password)
        if not password:
            abort(make_response(jsonify({'status': 400,
                                         ' error': "wrong password"}), 400))

        token = jwt.encode({"username":username}, KEY, algorithm='HS256')
        return jsonify({"status": 200, "token":token.decode('UTF-8'),
                        "message": "Logged in successfully"}), 200

    except psycopg2.DatabaseError as error:
        abort(make_response(jsonify(message="Server error : {}".format(error)), 500))
