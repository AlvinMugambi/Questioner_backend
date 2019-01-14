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

        self.signup_user = {"firstname":"obi",
                            "lastname": "wan",
                            "username":"obiwanca",
                            "email":"canobiedw@gmail.com",
                            "password": "ObiLigh1",
                            "confirm_password":"ObiLigh1"}
        self.login_user = {"username":"obiwanca",
                           "password":"ObiLigh1"}

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

        self.post_question3 = {"title":"what are languages?",
                               "body":"I would like to know this"}

        self.post_comment = {"comment":"I would love to hear this question answered"}

        self.question_and_comment = {"body": "I would like to know this",
                                     "comments": ["I would love to hear this question answered", {"username": "obiwanca"}],
                                     "meetup_id": 1,
                                     "question_id": 1,
                                     "title": "what are languages?",
                                     "votes": 0}


        self.upvoted_question = {"body": "I would like to know the kind of food being served at the meetup",
                                 "meetup_id": 1,
                                 "comments": [],
                                 "question_id": 1,
                                 "title": "what are we to eat?",
                                 "votes": 1}

        self.downvoted_question = {"body": "I would like to know the kind of food being served at the meetup",
                                   "meetup_id": 1,
                                   "comments": [],
                                   "question_id": 1,
                                   "title": "what are we to eat?",
                                   "votes": -1}
        self.token = ''

    def tearDown(self):
        """The tear down method that deletes records after tests run"""
        self.app.testing = False

class TestQuestionEndpoint(QuestionBaseTest):
    """
    Contains the test methods that assert the endpoints are working
    """
    def login(self):
        self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.signup_user),
            content_type="application/json")
        login = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.login_user),
            content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token


    def test_user_can_post_a_question(self):
        """
        test to show a user can successfully post a question
        """
        self.token = self.login()
        self.client.post("api/v1/meetups",
                         data=json.dumps(self.meetup),
                         content_type="application/json")
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
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
        self.token = self.login()
        self.client.post("api/v1/meetups",
                         data=json.dumps(self.meetup),
                         content_type="application/json")
        self.client.post("api/v1/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.patch("api/v1/questions/1/upvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_downvote_question(self):
        """
        test a user can upvote a question
        """
        self.token = self.login()
        self.client.post("api/v1/meetups",
                         data=json.dumps(self.meetup),
                         content_type="application/json")
        self.client.post("api/v1/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.patch("api/v1/questions/1/downvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_get_all_questions(self):
        """
        Test a user can get all the questions posted to a meetup
        """
        self.token = self.login()
        self.client.post("api/v1/meetups",
                         data=json.dumps(self.meetup),
                         content_type="application/json")
        self.client.post("api/v1/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v1/meetups/1/questions",
                         data=json.dumps(self.post_question2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v1/meetups/1/questions",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_comment_on_a_question(self):
        """
        Test to show a user can comment on a specific question
        """
        self.token = self.login()
        self.client.post("api/v1/meetups",
                         data=json.dumps(self.meetup),
                         content_type="application/json")
        self.client.post("api/v1/meetups/1/questions",
                         data=json.dumps(self.post_question3),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v1/questions/1/comment",
                                    data=json.dumps(self.post_comment),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf'8"))
        self.assertEqual(result['data'], self.question_and_comment)

    def test_token_missing(self):
        """
        test a user cannot post a question if not logged in
        """
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Token is missing")

    def test_token_is_invalid(self):
        """
        test a user cannot post a question if not logged in
        """
        token = "aduneoneuaounwLJNWEOI23E239P422O2423"
        response = self.client.post("api/v1/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], "Token is expired or invalid")
