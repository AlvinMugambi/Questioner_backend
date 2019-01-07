"""Creates the app instance and returns the app """

from flask import Flask
from app.api.v1.views.meetup_views import version1 as meetups

def create_app():
    """Creates the app instance and returns the app """
    app = Flask(__name__)
    app.register_blueprint(meetups)
    return app
