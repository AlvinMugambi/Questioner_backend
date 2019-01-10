"""The questions routes tests"""

import json
import unittest

# local imports
from app import create_app

class QuestionBaseTest(unittest.TestCase):
    """
    The base class for setting up and tearing down the Tests
    """

    def setUp(self):
        """
        sets the variables that run before each test
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.meetup = {"topic":"Python",
                       "meetup_date":"3/01/1991",
                       "location":"Nyeri",
                       "images":["them.png", "they.png"],
                       "tags":["Snake", "Camel"]
                      }

        self.post_question1 = {"title":"what are we to eat?",
                               "body":"I would like to know the kind of food being served at the meetup"}

        self.post_question2 = {"title":"what are the different extensions in flask?",
                               "body":"I would like to know the various flask extensions"}


        self.upvoted_question = {"body": "I would like to know the kind of food being served at the meetup",
                                 "meetup_id": 1,
                                 "question_id": 1,
                                 "title": "what are we to eat?",
                                 "votes": 1}

        self.downvoted_question = {"body": "I would like to know the kind of food being served at the meetup",
                                   "meetup_id": 1,
                                   "question_id": 1,
                                   "title": "what are we to eat?",
                                   "votes": -1}

    def tearDown(self):
        """The tear down method that deletes records after tests run"""
        self.app.testing = False

class TestQuestionEndpoint(QuestionBaseTest):
    """
    Contains the test methods that assert the endpoints are working
    """
    def test_user_can_post_a_question(self):
        """
        test to show a user can successfully post a question
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        response = self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), content_type = "application/json")
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'], [{"body": "I would like to know the kind of food being served at the meetup",
                                           "meetup": 1,
                                           "title": "what are we to eat?"}])

    def test_upvote_question(self):
        """
        test a user can upvote a question
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), content_type = "application/json")
        response = self.client.patch("api/v1/questions/1/upvote", content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.upvoted_question)

    def test_downvote_question(self):
        """
        test a user can upvote a question
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), content_type = "application/json")
        response = self.client.patch("api/v1/questions/1/downvote", content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.downvoted_question)

    def test_get_all_questions(self):
        """
        Test a user can get all the questions posted to a meetup
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question1), content_type = "application/json")
        self.client.post("api/v1/meetups/1/questions", data = json.dumps(self.post_question2), content_type = "application/json")
        response = self.client.get("api/v1/meetups/1/questions", content_type = "application/json")
        self.assertEqual(response.status_code, 200)
