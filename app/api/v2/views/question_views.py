"""The Question routes"""

from flask import jsonify, request, make_response, abort

from app.api.v2.models.models import Question, Comment, User, Meetup, Vote
from app.api.v2.models import database
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
            'status': 401,
            'error': "Please login first"}), 401

    try:
        data = request.get_json()
        title = data['title']
        body = data['body']

    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error': "Check your json keys. Should be topic and body"}), 400))

    validators.check_for_whitespace(data)
    meetup = Meetup.get_meetup(meetup_id)
    if not meetup:
        abort(make_response(jsonify({
            'status': 404,
            'error': 'No meetup with id {} found'.format(meetup_id)}), 404))

    user_id = user['user_id']
    question_asked = validators.check_if_question_asked(title, user_id)
    if question_asked:
        abort(make_response(jsonify({
            'status': 409,
            'error': 'You already asked this question'}), 409))

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


@version2.route("/questions/<int:question_id>/<vote>", methods=['PATCH'])
@token_required
def upvote_downvote_question(current_user, question_id, vote):
    """
    The upvote and downvote question route endpoint
    """
    username_dict = validators.decode_token()
    username = username_dict['username']
    user = User.get_user_by_username(username)
    try:
        user = user[0]
    except:
        return jsonify({
            'status': 401,
            'error': "Please login first"}), 401

    if vote not in ['upvote', 'downvote']:
        abort(make_response(jsonify({
            'status': 400,
            'error': 'url vote should be upvote or downvote'}), 400))

    question = Question.get_question(question_id)
    if question:
        user_id = user['user_id']
        voted = Vote.check_if_already_voted(user_id, question_id)
        if voted:
            abort(make_response(jsonify({
                'status': 409,
                'error': "You cannot vote twice on a single question"}), 409))

        my_question = question[0]
        if vote == 'upvote':
            my_question['votes'] = my_question['votes'] + 1
        if vote == 'downvote':
            my_question['votes'] = my_question['votes'] - 1

        query = """
        UPDATE questions SET votes = '{}' WHERE questions.question_id = '{}'
        """.format(my_question['votes'], question_id)
        database.query_db_no_return(query)

        voter = Vote(question_id=question_id,
                     user_id=user_id)
        voter.save_vote()
        return jsonify({"status": 200,
                        "data": {"questionId": my_question['question_id'],
                                 "title": my_question['title'],
                                 "body": my_question['body'],
                                 "votes": my_question['votes']}}), 200
    return jsonify({
        "status": 404,
        "error": "Question with id {} not found".format(question_id)}), 404


@version2.route("/meetups/<int:meet_id>/questions", methods=['GET'])
def get_all_questions_for_a_meetup(meet_id):
    """
    The get all questions for a specific meetup route endpoint
    """
    meetup = Meetup.get_meetup(meet_id)
    if not meetup:
        abort(make_response(jsonify({
            'status': 404,
            'error': 'Meetup with id {} not found'.format(meet_id)
        }), 404))
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
            'status': 401,
            'error': "Please login first"}), 401
    try:
        data = request.get_json()
    except KeyError:
        abort(make_response(jsonify({
            'status': 400,
            'error':'Check your json key. Should be comment'})))

    validators.check_for_whitespace(data)
    comment = data['comment']

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

        return jsonify({"status": 201,
                        "data": {"title": my_comment.title,
                                 "body": my_comment.body,
                                 "comment": my_comment.comment,
                                 "userId": my_comment.user_id,
                                 "question_id": my_comment.question_id,}}), 201
    return jsonify({
        'status': 404,
        'error':'Question with id {} not found'.format(question_id)}), 404


@version2.route("/questions/<int:question_id>/comments", methods=['GET'])
@token_required
def get_all_comments_on_a_question(current_user, question_id):
    """
    The get all comments on a question route endpoint
    """
    question = Question.get_question(question_id)
    if not question:
        abort(make_response(jsonify({
            'status': 404,
            'error': 'Question with id {} not found'.format(question_id)})))

    comments = Comment.get_all_comments(question_id)
    if comments:
        return jsonify({'status': 200,
                        'data': comments})
    question = question[0]
    return jsonify({
        'status': 404,
        'title': question['title'],
        'body': question['body'],
        'message' : 'No comments posted for question with id {}'.format(question_id)}), 404
