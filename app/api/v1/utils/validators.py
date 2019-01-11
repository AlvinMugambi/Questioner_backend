"""The validator functions that validate user data"""

import re

from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash

# local imports
from app.api.v1.models.models import USERS


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
            abort(make_response(jsonify(Message="Email already taken!"), 400))
    try:
        user, domain = str(email).split("@")
    except ValueError:
        abort(make_response(jsonify(message="Invalid Email"), 400))
    if not user or not domain:
        abort(make_response(jsonify(message="Invalid Email"), 400))

    # Check that domain is valid
    try:
        dom_1, dom_2 = domain.split(".")
    except ValueError:
        abort(make_response(jsonify(message="Invalid Email"), 400))
    if not dom_1 or not dom_2:
        abort(make_response(jsonify(message="Invalid Email"), 400))

    return email


def verify_password(password):
    if check_password_hash(hashed_password, password):
        pass
