"""The Question routes"""

from flask import jsonify, request, make_response, abort

from app.api.v2.models.models import Question, Comment, User, Meetup
from app.api.v2.utils.validators import token_required
from app.api.v2.utils import validators
from app.api.v2 import version2

@version2.route("/meetups/<int:meetup_id>/questions", methods=['POST'])
@token_required
def create_question(current_user, meetup_id):
    """
    The POST method for the questions route that allows a user to post a question
    """
    username_dict = validators.decode_token()
    username = username_dict['username']
    user = User.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 400,
            'error': "Please login first"}), 400

    try:
        data = request.get_json()
        title = data['title']
        body = data['body']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            ' error': "Check your json keys. Should be topic and body"}), 400))

    validators.check_for_whitespace(data)
    meetup = Meetup.get_meetup(meetup_id)
    if not meetup:
        abort(make_response(jsonify({
            'status': 404,
            'error': 'No meetup with id {} found'.format(meetup_id)}), 404))

    user_id = user['user_id']
    question = Question(user_id=user_id,
                        title=title,
                        body=body,
                        meetup_id=meetup_id)

    question.save_question()

    return jsonify({"status": 201,
                    "data":[{"title": title,
                             "user_id": user_id,
                             "meetup": meetup_id,
                             "body": body}]}), 201


@version2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
@token_required
def upvote_question(current_user, question_id):
    """
    The upvote question route endpoint
    """
    question = Question.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] + 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404


@version2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
@token_required
def downvote_question(current_user, question_id):
    """
    The downvote question route endpoint
    """
    question = Question.get_question(question_id)
    if question:
        my_question = question[0]
        my_question['votes'] = my_question['votes'] - 1
        return jsonify({"status": 200, "data": my_question}), 200
    return jsonify({"status": 404, "error": "Question not found"}), 404


@version2.route("/meetups/<int:meet_id>/questions", methods=['GET'])
def get_all_questions_for_a_meetup(meet_id):
    """
    The get all questions for a specific meetup route endpoint
    """
    questions = Question.get_all_questions(meet_id)
    if questions:
        return jsonify({"status": 200, "data": questions}), 200
    return jsonify({"status": 404,
                    "data": "No questions posted yet for this meetup"}), 404


@version2.route("/questions/<int:question_id>/comment", methods=['POST'])
@token_required
def comment_on_a_question(current_user, question_id):
    """
    The add comment to a question endpoint
    """
    username_dict = validators.decode_token()
    username = username_dict['username']
    user = User.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 400,
            'error': "Please login first"}), 400
    try:
        comment = request.get_json()['comment']
    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error':'Check your json key. Should be comment'})))


    question = Question.get_question(question_id)
    if question:
        question = question[0]
        user_id = user['user_id']
        title = question['title']
        body = question['body']

        my_comment = Comment(title,
                             body,
                             comment,
                             user_id,
                             question_id)
        my_comment.save_comment()

        return jsonify({"status": 201, "data": {"title": my_comment.title,
                                                "body": my_comment.body,
                                                "comment": my_comment.comment,
                                                "userId": my_comment.user_id,
                                                "question_id": my_comment.question_id,}}), 201
    return jsonify({
        'status': 404,
        'error':'Question with id {} not found'.format(question_id)}), 404
