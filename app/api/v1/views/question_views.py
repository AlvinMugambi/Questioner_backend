from flask import jsonify, request

from app.api.v1.models.models import Question, QUESTIONS
from app.api.v1 import version1

@version1.route("/meetups/<int:meetup_id>/questions", methods=['POST'])
def create_question(meetup_id):
    """
    The POST method for the questions route that allows a user to post a question
    """
    try:
        title = request.get_json()['title']
        body = request.get_json()['body']

    except:
        return jsonify({'status': 400,
                        ' error': "Check your json keys. Should be topic and body"})

    if not title:
        return jsonify({'status': 400,
                        'error': 'topic field is required'})

    if not body:
        return jsonify({'status': 400,
                        'error': 'body field is required'})

    question = Question(title=title,
                        body=body,
                        meetup_id=meetup_id)

    question.save_question()

    return jsonify({"status": 201,
                    "data":[{"title": title,
                             # "user_id": user_id,
                             "meetup": meetup_id,
                             "body": body}]}), 201
