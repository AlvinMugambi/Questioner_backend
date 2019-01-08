"""The meetup routes"""

from flask import jsonify, request

from app.api.v1.models.models import Meetup, MEETUPS
from app.api.v1 import version1

@version1.route("/meetups", methods=['POST'])
def create_meetup():
    """
    The POST method for the meetups route that allows a user to create a meetup
    """
    try:
        topic = request.get_json()['topic']
        meetup_date = request.get_json()['meetup_date']
        location = request.get_json()['location']
        images = request.get_json()['images']
        tags = request.get_json()['tags']

    except:
        return jsonify({'status':400,
                        'error': 'Check your json keys. Should be topic, meetup_date, location, images and tags'}), 400

    if not topic:
        return jsonify({'status':400, 'error':'topic field is required'}), 400
    if not meetup_date:
        return jsonify({'status':400, 'error':'meetup_date field is required'}), 400

    if not location:
        return jsonify({'status':400, 'error':'location field is required'}), 400

    if not tags:
        return jsonify({'status':400, 'error':'tags field is required'}), 400

    meetup = Meetup(
        topic=topic,
        meetup_date=meetup_date,
        location=location,
        images=images,
        tags=tags
    )
    meetup.save_meetup()

    return jsonify({"status": 201,
                    "data": [{"topic": topic,
                              "location": location,
                              "meetup_date": meetup_date,
                              "tags": tags}]}), 201

@version1.route("/meetups", methods=["GET"])
def get_meetups():
    """
    Fetches all meetups
    """
    meetups = Meetup.get_all_meetups()

    if meetups:
        return jsonify({"status": 200, "data": meetups}), 200
    return jsonify({
        "status": 404,
        "error": "Currently there are no meetups scheduled."
    }), 404
