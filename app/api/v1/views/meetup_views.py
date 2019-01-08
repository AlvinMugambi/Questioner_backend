from flask import Flask, jsonify, request
import datetime

from app.api.v1.models.models import meetups, Meetup
from app.api.v1 import version1

@version1.route("/meetups", methods=['POST'])
def create_meetup():
    try:
        topic = request.get_json()['topic']
        meetup_date = request.get_json()['meetup_date']
        location = request.get_json()['location']
        images = request.get_json()['images']
        tags= request.get_json()['tags']

    except:
        return jsonify({'Key Error': 'Check your json keys. Should be topic, meetup_date, location, images and tags'})

    if not topic:
        return jsonify({'Error':'topic fields is required'})

    if not meetup_date:
        return jsonify({'Error':'meetup_date fields is required'})

    if not location:
        return jsonify({'Error':'location fields is required'})

    if not tags:
        return jsonify({'Error':'tags fields is required'})

    meetup = Meetup(
        topic=topic,
        meetup_date=meetup_date,
        location=location,
        images=images,
        tags=tags
    )
    meetup.create_meetup()

    return jsonify({"status": 201, "data": [{"topic": topic, "location": location, "meetup_date": meetup_date, "tags": tags}]}), 201
