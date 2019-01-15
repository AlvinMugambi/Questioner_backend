"""
The meetups models
"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models import database

class User:
    """
    The user models
    """

    def __init__(self, username, email, password,
                 firstname, lastname, phone_number):
        """
        Define the user model and its attributes
        """

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = self.encrypt_password_on_signup(password)


    def save_user(self):
        """
        Add a new user to the users store
        """
        query = """
        INSERT INTO users(username, firstname, lastname, phoneNumber, email, password) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname, self.phone_number, self.email, self.password)

        database.query_db_no_return(query)

    @staticmethod
    def query_users(username):
        """
        Query the users store for a user
        """
        query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return database.select_from_db(query)

    @staticmethod
    def get_user_by_username(username):
        """
            Queries db for user with given username
            Returns user object
        """
        # Query db for user with those params
        query = """
        SELECT user_id, username, email, password FROM users
        WHERE users.username = '{}'""".format(username)

        return database.select_from_db(query)

    def encrypt_password_on_signup(self, password):
        """
        convert password to hashed on user login
        """
        hashed_password = generate_password_hash(str(password))
        return hashed_password

    @staticmethod
    def check_if_password_in_db(password_hash, password):
        """
        Check if input password and db passwords match
        """
        return check_password_hash(password_hash, str(password))


    @staticmethod
    def to_json(user):
        """
        format user object to a readable dictionary
        """
        return {"username": user.username,
                "email": user.email,
                "password": user.password,}


class Meetup:
    """
    The Meetup class that contains the meetup models
    """
    def __init__(self, topic, meetup_date, location, images, tags):
        """
        The initialization of the Meetup class that defines its variables
        """
        self.topic = topic
        self.meetup_date = meetup_date
        self.location = location
        self.images = images
        self.tags = tags
        self.created_at = datetime.now()

    def save_meetup(self):
        """
        saves new meetup to store
        """
        query = """
        INSERT INTO meetups(topic, meetup_date, meetup_location, meetup_images, meetup_tags, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.topic, self.meetup_date, self.location, self.images, self.tags, self.created_at)

        database.query_db_no_return(query)

    @staticmethod
    def get_all_meetups():
        """
        gets all meetups
        """
        return [Meetup.to_json(meetup) for meetup in MEETUPS]

    @staticmethod
    def get_meetup(meet_id):
        """
        get a specific meetup using its id
        """
        return [Meetup.to_json(meetup) for meetup in MEETUPS if meetup.id == meet_id]

    @staticmethod
    def delete_meetup(meet_id):
        """
        Delete a specific meetup in the db
        """
        found = None
        for meetup in MEETUPS:
            if meetup.id == meet_id:
                MEETUPS.remove(meetup)
                found = True
            elif meetup.id != meet_id:
                found = False
        return found


    @staticmethod
    def to_json(meetup):
        """
        format meetup object to a readable dictionary
        """
        return {
            "id": meetup.id,
            "topic": meetup.topic,
            "meetup_date": meetup.meetup_date,
            "location": meetup.location,
            # "images": meetup.images,
            "tags": meetup.tags,
            # "created_at": meetup.created_at
        }

class Question:
    """
    The question class that contains the questions models and methods
    """

    def __init__(self, title, body, meetup_id):
        """
        The initialization of the Question class that defines its variables
        """
        self.question_id = len(QUESTIONS)+1
        self.meetup_id = meetup_id
        self.title = title
        self.votes = 0
        self.body = body
        self.comments = COMMENTS
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        QUESTIONS.append(self)

    @staticmethod
    def get_all_questions(meet_id):
        """
        get all questions asked for a specific meetup
        """
        return [Question.to_json(question) for question in QUESTIONS if question.meetup_id == meet_id]


    @staticmethod
    def get_question(quest_id):
        """
        get a specific question using its id
        """
        return [Question.to_json(question) for question in QUESTIONS if question.question_id == quest_id]

    @staticmethod
    def to_json(question):
        """
        format question object to a readable dictionary
        """
        return {
            "question_id": question.question_id,
            "title": question.title,
            "meetup_id": question.meetup_id,
            "votes": question.votes,
            "body": question.body,
            "comments": question.comments}


class Comment:
    """
    The comments models
    """

    def __init__(self, comment, question_id):
        self.comment = comment
        # self.user_id = user_id
        self.comment_id = len(COMMENTS)+1
        self.question_id = question_id

    def save_comment(self):
        """
        Save the comment to the comments store
        """
        COMMENTS.append(self)

class Comment:
    """
    The comments models
    """

    def __init__(self, comment, question_id):
        self.comment = comment
        # self.user_id = user_id
        self.comment_id = len(COMMENTS)+1
        self.question_id = question_id

    def save_comment(self):
        """
        Save the comment to the comments store
        """
        COMMENTS.append(self)

    @staticmethod
    def to_json(comment):
        """
        format comment object to a readable dictionary
        """
        return {"comment":comment.comment,
                "comment_id":comment.comment_id,
                "question_id":comment.question}
