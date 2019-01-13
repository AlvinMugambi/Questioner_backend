"""The meetup routes"""

from flask import jsonify, request, make_response, abort

from app.api.v2.utils.validators import token_required, check_if_admin
from app.api.v2.models.models import Meetup
from app.api.v2 import version2

@version2.route("/meetups", methods=['POST'])
@token_required
def create_meetup(current_user):
    """
    The POST method for the meetups route that allows a user to create a meetup
    """
    try:
        topic = request.get_json()['topic']
        meetup_date = request.get_json()['meetup_date']
        location = request.get_json()['location']
        images = request.get_json()['images']
        tags = request.get_json()['tags']

    except KeyError:
        return jsonify({'status':400,
                        'error': 'Check your json keys. Should be topic, meetup_date, location, images and tags'}), 400

    if not topic:
        abort(make_response(jsonify({'status':400, 'error':'topic field is required'}), 400))
    if not meetup_date:
        abort(make_response(jsonify({'status':400, 'error':'meetup_date field is required'}), 400))

    if not location:
        abort(make_response(jsonify({'status':400, 'error':'location field is required'}), 400))

    if not tags:
        abort(make_response(jsonify({'status':400, 'error':'tags field is required'}), 400))

    admin = check_if_admin()
    if not admin:
        return jsonify({'status': 401, 'error':"You are not allowed to perfom this function"}), 401

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


@version2.route("/meetups/upcoming", methods=["GET"])
def get_meetups():
    """
    Fetches all meetups
    """
    meetups = Meetup.get_all_meetups()

    if meetups:
        return jsonify({"status": 200, "data": meetups}), 200
    return jsonify({
        "status": 404,
        "data": "Currently there are no meetups scheduled."
    }), 404


@version2.route("/meetups/<int:meetup_id>", methods=["GET"])
def get_single_meetup(meetup_id):
    """
    Fetches a single meetup
    """
    meetup = Meetup.get_meetup(meetup_id)
    if meetup:
        return jsonify({"status": 200, "data": meetup}), 200
    return jsonify({"status": 404, "data": "Meetup not found"}), 404

@version2.route("/meetups/<int:meetup_id>/rsvps/<resp>", methods=['POST'])
def meetup_rsvp(meetup_id, resp):
    """
    A user can respond to a meetup rsvp
    """
    if resp not in ["yes", "no", "maybe"]:
        return jsonify({'status':400, 'error':'Response should be either yes, no or maybe'}), 400
    meetup = Meetup.get_meetup(meetup_id)
    if not meetup:
        return jsonify({'status': 404, 'error':'Meetup with id {} not found'.format(meetup_id)}), 404
    meetup = meetup[0]
    return jsonify({'status':200, 'data':[{'meetup':meetup_id,
                                           'topic':meetup['topic'],
                                           'Attending':resp}]}), 200

@version2.route("/meetups/<int:meetup_id>", methods=['DELETE'])
@token_required
def delete_a_meetup(current_user, meetup_id):
    """
    The endpoint that allows a user to delete a meetup
    """
    admin = check_if_admin()
    if not admin:
        return jsonify({'status': 401, 'error':"You are not allowed to perfom this function"}), 401

    deleted = Meetup.delete_meetup(meetup_id)

    if deleted:
        return jsonify({'status': 200, 'data':"Deleted successfully"}), 200
    return jsonify({'status': 404, 'data':"Meetup with id {} not found".format(meetup_id)}), 404
