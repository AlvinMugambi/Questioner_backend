"""
Creates the app function and returns the app
"""

# standard imports
from flask import Flask, Blueprint, jsonify

from app.api.v1.views.meetup_views import version1 as meetups
from app.api.v1.views.question_views import version1 as questions
from app.api.v1.views.user_views import version1 as users
from config import app_config



def create_app(app_environment):
    """Creates the app instance and returns the app """
    app = Flask(__name__)
    app.config.from_object(app_config[app_environment])
    app.register_blueprint(meetups)
    app.register_blueprint(questions)
    app.register_blueprint(users)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error':'Url not found', 'status': 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error':'Method not allowed', 'status': 405}), 405

    return app
