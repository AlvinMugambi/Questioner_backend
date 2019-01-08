"""
Creates the app function and returns the app
"""

# local imports
from flask import Flask, Blueprint

from app.api.v1.views.meetup_views import version1 as meetups
from config import app_config


def create_app(app_environment):
    """Creates the app instance and returns the app """
    app = Flask(__name__)
    app.config.from_object(app_config[app_environment])
    app.register_blueprint(meetups)

    return app
