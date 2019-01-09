"""
The meetups models
"""

from datetime import datetime

MEETUPS = []
QUESTIONS = []


class Meetup:
    """
    The Meetup class that contains the meetup models
    """
    def __init__(self, topic, meetup_date, location, images, tags):
        """
        The initialization of the Meetup class that defines its variables
        """
        self.id = len(MEETUPS)+1
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
        MEETUPS.append(self)

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
        self.created_at = datetime.now()

    def save_question(self):
        """
        saves the question to the question store
        """
        QUESTIONS.append(self)

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
        }
    @staticmethod
    def get_question(quest_id):
        """
        get a specific question using its id
        """
        return [Question.to_json(question) for question in QUESTIONS if question.question_id == quest_id]
