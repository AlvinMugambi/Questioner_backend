from flask import request, jsonify, abort, make_response

from app.api.v1.models.models import User, USERS
from app.api.v1 import version1

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
                                     ' error': "Check your json keys"}), 400))

    if password != confirm_pass:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Passwords don't match"}), 400))

    user = User(firstname=firstname,
                username=username,
                lastname=lastname,
                email=email,
                password=password)

    user.save_user()
    return jsonify({"status":201, "data":"Registered successfully!"})


@version1.route("/auth/login", methods=['POST'])
def user_login():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Check your json keys. Should be username & password"}), 400))

    user = User.query_users(username, password)
    if user:
        return jsonify({"status": 200, "data":"Logged in successfully"}), 200
    return jsonify({"status": 400, "data":"Register first"}), 400
