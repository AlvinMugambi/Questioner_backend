"""The Question routes"""

from flask import jsonify, request, make_response, abort

from app.api.v1.models.models import Question
from app.api.v1 import version1

@version1.route("/meetups/<int:meetup_id>/questions", methods=['POST'])
def create_question(meetup_id):
    """
    The POST method for the questions route that allows a user to post a question
    """
    try:
        title = request.get_json()['title']
        body = request.get_json()['body']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Check your json keys. Should be topic and body"}), 400))

    if not title:
        abort(make_response(jsonify({'status': 400,
                                     'error': 'topic field is required'}), 400))

    if not body:
        abort(make_response(jsonify({'status': 400,
                                     'error': 'body field is required'}), 400))

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


@version1.route("/meetups/<int:meet_id>/questions", methods=['GET'])
def get_all_questions_for_a_meetup(meet_id):
    """
    The get all questions for a specific meetup route endpoint
    """
    questions = Question.get_all_questions(meet_id)
    if questions:
        return jsonify({"status": 200, "data": questions}), 200
    return jsonify({"status": 404, "data": "No questions posted yet for this meetup"}), 404


@version1.route("/questions/<int:question_id>/comment", methods=['POST'])
def comment_on_a_question(question_id):
    """
    The add comment to a question endpoint
    """
    try:
        comment = request.get_json()['comment']
    except KeyError:
        abort(make_response(jsonify({'status': 400, 'error':'Check your json key. Should be comment'})))

    question = Question.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['comments'].append(comment)
        return jsonify({"status": 201, "data": my_question}), 201
    return jsonify({'status': 404, 'error':'Question not found'}), 404
