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
                 firstname, lastname, phone):
        """
        Define the user model and its attributes
        """

        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.password = self.encrypt_password_on_signup(password)


    def save_user(self):
        """
        Add a new user to the users store
        """
        query = """
        INSERT INTO users(username, firstname, lastname,
                          phone, email, password) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname,
                    self.phone, self.email, self.password)

        database.query_db_no_return(query)


    @staticmethod
    def get_user_by_username(username):
        """
            Queries db for user with given username
            Returns user object
        """
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
    def get_user_questions(user_id):
        """
        Get all the questions a user has posted
        """
        query = """
        SELECT question_id FROM questions
        WHERE questions.user_id = '{}'""".format(user_id)

        questions_list = database.select_from_db(query)
        questions = len(questions_list)
        return questions

    @staticmethod
    def get_user_commented_questions(user_id):
        """
        Get all the questions a user has posted
        """
        query = """
        SELECT question_id FROM comments
        WHERE comments.user_id = '{}'""".format(user_id)

        comments_list = database.select_from_db(query)
        data = set()
        for listed in comments_list:
            for lists in listed:
                data.add(lists)
        comments = len(data)
        return comments

    @staticmethod
    def get_user_meetups(user_id):
        """
        Get all the meetups a user has purposed to attend
        """
        query = """
        SELECT meetup_id, meetup_topic FROM rsvps
        WHERE rsvps.user_id = '{}' AND rsvps.rsvp = '{}'
        """.format(user_id, 'yes')

        meetups = database.select_from_db(query)
        return meetups


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
        INSERT INTO meetups(topic, meetup_date, meetup_location,
                            meetup_images, meetup_tags, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.topic, self.meetup_date, self.location,
                    self.images, self.tags, self.created_at)

        database.query_db_no_return(query)

    @staticmethod
    def get_all_meetups():
        """
        gets all meetups
        """
        query = """
        SELECT meetup_id, topic, meetup_date, meetup_location,
        meetup_tags, created_at FROM meetups
        """

        meetups = database.select_from_db(query)
        data = []
        for meetup in meetups:
            meetup = {'meetupId' : meetup["meetup_id"],
                      'topic' : meetup["topic"],
                      'meetupDate' : meetup["meetup_date"],
                      'meetupLocation' : meetup["meetup_location"],
                      'meetupTags' : meetup["meetup_tags"],
                      'createdAt' : meetup["created_at"]}
            data.append(meetup)

        return data

    @staticmethod
    def get_meetup(meet_id):
        """
        get a specific meetup using its id
        """
        query = """
        SELECT meetup_id, topic, meetup_date, meetup_location FROM meetups
        WHERE meetups.meetup_id = '{}'""".format(meet_id)

        meetup = database.select_from_db(query)
        return meetup

    @staticmethod
    def check_if_meetup_already_posted(meetup_location, date):
        """
        The function that checks if a user has already posted on a meetup
        """
        query = """
        SELECT meetup_id FROM meetups
        WHERE meetups.meetup_location = '{}' AND meetups.meetup_date = '{}'
        """.format(meetup_location, date)

        posted = database.select_from_db(query)
        return posted

    @staticmethod
    def delete_meetup(meet_id):
        """
        Delete a specific meetup in the db
        """
        meetup = Meetup.get_meetup(meet_id)

        if meetup:
            query = """
            DELETE FROM meetups
            WHERE meetups.meetup_id = '{}'""".format(meet_id)

            database.query_db_no_return(query)
            return True
        return False


class Question:
    """
    The question class that contains the questions models and methods
    """

    def __init__(self, user_id, title, body, meetup_id, votes=0):
        """
        The initialization of the Question class that defines its variables
        """
        self.user_id = user_id
        self.meetup_id = meetup_id
        self.title = title
        self.body = body
        self.votes = votes
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        query = """
        INSERT INTO questions(user_id, meetup_id, title,
                              body, votes, created_at) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.meetup_id, self.title,
                    self.body, self.votes, self.created_at)

        database.query_db_no_return(query)


    @staticmethod
    def get_all_questions(meet_id):
        """
        get all questions asked for a specific meetup
        """
        query = """
        SELECT question_id, user_id, meetup_id, title,
        body, votes, created_at FROM questions
        WHERE questions.meetup_id = '{}'
        """.format(meet_id)

        questions = database.select_from_db(query)
        data = []
        for question in questions:
            question = {'questionId' : question["question_id"],
                        'userId' : question["user_id"],
                        'meetupId' : question["meetup_id"],
                        'title' : question["title"],
                        'body' : question["body"],
                        'votes' : question["votes"],
                        'createdAt' : question["created_at"]
                       }
            data.append(question)

        return data


    @staticmethod
    def get_question(quest_id):
        """
        get a specific question using its id
        """
        query = """
        SELECT question_id, title, body, comment, votes FROM questions
        WHERE questions.question_id = '{}'""".format(quest_id)

        question = database.select_from_db(query)
        return question


class Comment:
    """
    The comments models
    """

    def __init__(self, title, body, comment, user_id, question_id):
        self.title = title
        self.body = body
        self.comment = comment
        self.user_id = user_id
        self.question_id = question_id

    def save_comment(self):
        """
        Save the comment to the comments store
        """
        query = """
        INSERT INTO comments(user_id, question_id, title, body, comment) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.user_id, self.question_id, self.title,
                    self.body, self.comment)

        database.query_db_no_return(query)


    @staticmethod
    def get_all_comments(quest_id):
        """
        get all comments asked for a specific question
        """
        query = """
        SELECT user_id, question_id, title, body, comment FROM comments
        WHERE comments.question_id = '{}'
        """.format(quest_id)

        comments = database.select_from_db(query)
        data = []
        for comment in comments:
            comment = {'userId' : comment["user_id"],
                       'questionId' : comment["question_id"],
                       'title' : comment["title"],
                       'body' : comment["body"],
                       'comment' : comment["comment"],
                      }
            data.append(comment)

        return data


class Rsvp:
    """
    The rsvp models
    """

    def __init__(self, meetup_id, user_id, meetup_topic, rsvp):
        """
        The initializer function that sets the rsvp variables
        """
        self.meetup_id = meetup_id
        self.user_id = user_id
        self.meetup_topic = meetup_topic
        self.rsvp = rsvp


    def save_rsvp(self):
        """
        Save the rsvp to the rsvps store
        """
        query = """
        INSERT INTO rsvps(meetup_id, user_id, meetup_topic, rsvp) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.meetup_id, self.user_id, self.meetup_topic, self.rsvp)

        database.query_db_no_return(query)


    @staticmethod
    def update_rsvp(meetup_id, user_id):
        """
        remove a yes response when the same user cancels attendance
        """
        query = """
        UPDATE rsvps SET rsvp = '{}' WHERE rsvps.meetup_id = '{}'
        AND rsvps.user_id = '{}'
        """.format('no', meetup_id, user_id)

        database.query_db_no_return(query)


    @staticmethod
    def get_attendees(meetup_id):
        """
        Get the number of people who have confirmed to attend a meetup
        """
        query = """
        SELECT rsvp_id FROM rsvps
        WHERE rsvps.meetup_id = '{}' AND rsvps.rsvp = '{}'
        """.format(meetup_id, 'yes')

        attendees_list = database.select_from_db(query)
        attendees = len(attendees_list)
        return attendees


class Vote:
    """
    The votes models
    """

    def __init__(self, question_id, user_id):
        """
        The initializer function that sets the votes variables
        """
        self.question_id = question_id
        self.user_id = user_id


    def save_vote(self):
        """
        Save the votes to the votes store
        """
        query = """
        INSERT INTO votes(user_id, question_id) VALUES(
            '{}', '{}'
        )""".format(self.user_id, self.question_id)

        database.query_db_no_return(query)


    @staticmethod
    def check_if_already_voted(user_id, question_id):
        """
        The function that checks if a user has already voted on a question
        """
        query = """
        SELECT user_id, question_id FROM votes
        WHERE votes.user_id = '{}' AND votes.question_id = '{}'
        """.format(user_id, question_id)

        voted = database.select_from_db(query)
        return voted

class Token:
    """
    The token class object
    """
    def __init__(self, token):
        """
        The initializer function that sets he token variables
        """
        self.token = token

    def blacklist_token(self):
        """
        Save the token to the blacklist token table
        """
        query = """
        INSERT INTO blacklist_tokens(token) VALUES(
            '{}'
        )""".format(self.token)

        database.query_db_no_return(query)

    @staticmethod
    def check_if_token_blacklisted(token):
        """
        Check if the token a user is using is blacklisted
        """
        query = """
        SELECT token FROM blacklist_tokens
        WHERE blacklist_tokens.token = '{}'
        """.format(token)

        token = database.select_from_db(query)
        return token
