"""Creates the app instance and returns the app """

from flask import Flask

def create_app():
    """Creates the app instance and returns the app """
    app = Flask(__name__)

    return app
