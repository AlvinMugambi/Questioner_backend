"""
Creates the app function and returns the app
"""

# standard imports
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

from app.api.v2.views.meetup_views import version2 as meetups2
from app.api.v2.views.question_views import version2 as questions2
from app.api.v2.views.user_views import version2 as users2
from app.api.v2.models.database import init_db
from config import app_config



def create_app(app_environment):
    """Creates the app instance and returns the app """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[app_environment])
    app.register_blueprint(meetups2)
    app.register_blueprint(questions2)
    app.register_blueprint(users2)
    init_db(app_config["db_url"])
    CORS(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error':'Url not found. Check your url and try again', 'status': 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error':'Method not allowed', 'status': 405}), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error':'Bad request. Check the syntax', 'status': 400}), 400

    return app
