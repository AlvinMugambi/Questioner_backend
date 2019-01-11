import os
import jwt
from flask import request, jsonify, abort, make_response
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v1.utils.validators import validate_email, check_password
from app.api.v1.models.models import User
from app.api.v1 import version1

KEY = os.getenv('SECRET_KEY')

@version1.route("/auth/signup", methods=['POST'])
def user_sign_up():
    try:
        firstname = request.get_json()['firstname']
        lastname = request.get_json()['lastname']
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        confirm_pass = request.get_json()['confirm_password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     'error': "Check your json keys"}), 400))

    check_password(password, confirm_pass)
    email = validate_email(email)

    user = User(firstname=firstname,
                username=username,
                lastname=lastname,
                email=email,
                password=password)

    user.save_user()
    return jsonify({"status":201, "data":"Registered successfully!"}), 201


@version1.route("/auth/login", methods=['POST'])
def user_login():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Check your json keys. Should be username & password"}), 400))

    user = User.query_users(username, password)
    if not user:
        return jsonify({"status": 400, "data":"Register first"}), 400

    token = jwt.encode({"username":username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, KEY, algorithm='HS256')
    return jsonify({"status": 200, "data":token.decode('UTF-8')}), 200
