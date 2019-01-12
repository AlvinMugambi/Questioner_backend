"""
Creates the app function and returns the app
"""

# standard imports
from flask import Flask, Blueprint

from app.api.v1.views.meetup_views import version1 as meetups
from app.api.v1.views.question_views import version1 as questions
from app.api.v1.views.user_views import version1 as users
# from app.api.v2.views.meetup_views import version2 as meetups2
# from app.api.v2.views.question_views import version2 as questions2
from app.api.v2.views.user_views import version2 as users2
from app.api.v2.models.database import init_db
from config import app_config



def create_app(app_environment):
    """Creates the app instance and returns the app """
    app = Flask(__name__)
    app.config.from_object(app_config[app_environment])
    app.register_blueprint(meetups)
    app.register_blueprint(questions)
    app.register_blueprint(users)
    # app.register_blueprint(meetups2)
    # app.register_blueprint(questions2)
    app.register_blueprint(users2)
    init_db(app_config["db_url"])

    return app
