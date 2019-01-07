from flask import jsonify,

from app.api.v1 import version1

@version1.route("/meetups", methods= ['POST'])
def create_meetup():
    pass
