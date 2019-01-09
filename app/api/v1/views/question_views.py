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


@version1.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
def upvote_question(question_id):
    """
    The upvote question route endpoint
    """
    question = Question.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] + 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404


@version1.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
def downvote_question(question_id):
    """
    The downvote question route endpoint
    """
    question = Question.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] - 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404
