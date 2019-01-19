import os
import jwt
from flask import request, jsonify, abort, make_response
import psycopg2
import datetime

from app.api.v2.utils import validators
from app.api.v2.utils.validators import token_required
from app.api.v2.models.models import User, Token
from app.api.v2 import version2

KEY = os.getenv('SECRET_KEY')

@version2.route("/auth/signup", methods=['POST'])
def user_sign_up():
    try:
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        password = data['password']
        confirmPass = data['confirmpassword']
        phone = data['phoneNumber']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error': "Should be firstname, lastname, username, email, password, confirmpassword and phoneNumber"}), 400))


    validators.check_for_whitespace(data)
    validators.check_if_string(data)
    validators.check_phone_number(phone)
    validators.check_password(password, confirmPass)
    email = validators.validate_email(email)

    validators.check_duplication({"username": username}, "users")
    validators.check_duplication({"email": email}, "users")

    user = User(firstname=firstname,
                lastname=lastname,
                phone=phone,
                username=username,
                email=email,
                password=password)

    user.save_user()
    return jsonify({"status":201, "data":"Registered successfully!"}), 201


@version2.route("/auth/login", methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error': "Should be username & password"}), 400))


    validators.check_for_whitespace(data)

    try:
        user = User.get_user_by_username(username)
        if not user:
            return jsonify({"status": 400,
                            "data":"The username or passsword is incorrect"}), 400

        username = user[0][1]
        hashed_password = user[0][3]

        password = User.check_if_password_in_db(hashed_password, password)
        if not password:
            abort(make_response(jsonify({'status': 400,
                                         'error': "wrong password"}), 400))

        token = jwt.encode({"username":username,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                           KEY, algorithm='HS256')
        return jsonify({"status": 200, "token":token.decode('UTF-8'),
                        "message": "Logged in successfully"}), 200

    except psycopg2.DatabaseError as error:
        abort(make_response(jsonify(message="Server error : {}".format(error)), 500))


@version2.route("/profile", methods=['GET'])
@token_required
def user_profile(current_user):
    username_dict = validators.decode_token()
    username = username_dict['username']
    user = User.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 401,
            'error': "Please login first"}), 401

    user_id = user['user_id']
    questions = User.get_user_questions(user_id)
    meetups = User.get_user_meetups(user_id)
    data = []
    for meetup in meetups:
        meetup = {'meetupId': meetup['meetup_id'],
                  'meetupTopic': meetup['meetup_topic']}
        data.append(meetup)

    return jsonify({"status": 200,
                    "data":{'questions' : questions,
                            'meetups': data}}), 200


@version2.route("auth/logout", methods=["POST"])
@token_required
def logout(current_user):
    """
    The logout route endpoint
    """
    token = request.headers['x-access-token']

    blacklist_token = Token(token=token)
    blacklist_token.blacklist_token()

    return jsonify({'status': 200,
                    'data': 'Logged out successfully'}), 200
