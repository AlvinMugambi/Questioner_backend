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

        self.post_question1 = {"meetup":1,
                               "title":"what are we to eat?",
                               "body":"I would like to know the kind of food being served at the meetup"}




class TestQuestionEndpoint(QuestionBaseTest):
    """
    Contains the test methods that assert the endpoints are working
    """
    def test_user_can_post_a_question(self):
        """
        test to show a user can successfully post a question
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.meetup), content_type = "application/json")
        response = self.client.post("api/v1/questions", data = json.dumps(self.post_question1), content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'], self.post_question1)
