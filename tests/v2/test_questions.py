"""The questions routes tests"""

import json
import unittest

# local imports
from app import create_app
from config import app_config
from app.api.v2.models.database import init_db

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
        # Retrieve test_db url from env
        self.db_url = app_config['test_db_url']
        # initialize db, create tables
        init_db(self.db_url)

        self.signup_admin = {"firstname":"obi",
                             "lastname": "wan",
                             "username":"iamtheadmin",
                             "email":"cano@gmail.com",
                             "password": "ThaOG1234",
                             "confirmpassword":"ThaOG1234",
                             "phoneNumber": "0729434944"}

        self.login_admin = {"username":"iamtheadmin",
                            "password":"ThaOG1234"}

        self.signup_user = {"firstname":"obi",
                            "lastname": "wan",
                            "username":"obiwan",
                            "email":"canobi@gmail.com",
                            "password": "ObiLight1",
                            "confirmpassword":"ObiLight1",
                            "phoneNumber": "0729434944"}
        self.login_user = {"username":"obiwan",
                           "password":"ObiLight1"}

        self.meetup = {"topic":"Python",
                       "meetup_date":"03/01/2091",
                       "location":"Nyeri",
                       "images":"them.png",
                       "tags":"Snake"}

        self.post_question1 = {
            "title":"what are we to eat?",
            "body":"I would like to know the kind of food being served at the meetup"}

        self.post_question2 = {
            "title":"what are the different extensions in flask?",
            "body":"I would like to know the various flask extensions"}

        self.post_question3 = {
            "title":"what are languages?",
            "body":"I would like to know this"}

        self.post_wrong_keys = {
            "ti":"what are we to eat?",
            "boy":"I would like to know the kind of food being served at the meetup"}

        self.post_comment = {"comment":"I would love to hear this question answered"}

        self.question_and_comment = {
            "body": "I would like to know this",
            "comment": "I would love to hear this question answered",
            "question_id": 1,
            "title": "what are languages?",
            "userId": 1}

        self.upvoted_question = {
            "body": "I would like to know the kind of food being served at the meetup",
            "comment": None,
            "questionId": 1,
            "title": "what are we to eat?",
            "votes": 1}

        self.downvoted_question = {
            "body": "I would like to know the kind of food being served at the meetup",
            "comment": None,
            "questionId": 1,
            "title": "what are we to eat?",
            "votes": 0}

        self.token = ''

    def tearDown(self):
        """The tear down method that deletes records after tests run"""
        self.app.testing = False
        init_db(self.db_url)


class TestQuestionEndpoint(QuestionBaseTest):
    """
    Contains the test methods that assert the endpoints are working
    """
    def login(self):
        """
        Login admin in to get token
        """
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_admin),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token


    def test_wrong_json_keys_on_input(self):
        """
        test user input wrong keys
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/questions",
                                    data=json.dumps(self.post_wrong_keys),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'], "Check your json keys. Should be topic and body")


    def test_no_meetup_found(self):
        """
        test to show a user cannot post a question to a not posted meetup
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 404)
        self.assertEqual(result['error'], 'No meetup with id 1 found')


    def test_user_can_post_a_question(self):
        """
        test to show a user can successfully post a question
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/questions",
                                    data=json.dumps(self.post_question1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(
            result['data'],
            [{"body": "I would like to know the kind of food being served at the meetup",
              "meetup": 1,
              "title": "what are we to eat?",
              "user_id": 1}])


    def test_get_all_questions(self):
        """
        Test a user can get all the questions posted to a meetup
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v2/meetups/1/questions",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_comment_on_a_question(self):
        """
        Test to show a user can comment on a specific question
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question3),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/questions/1/comment",
                                    data=json.dumps(self.post_comment),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf'8"))
        self.assertEqual(result['data'], self.question_and_comment)


    def test_upvote_question(self):
        """
        test a user can upvote a question
        """
        self.token = self.login()
        y = self.client.post("api/v2/meetups",
                             data=json.dumps(self.meetup),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(y.status_code, 201)
        x = self.client.post("api/v2/meetups/1/questions",
                             data=json.dumps(self.post_question1),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(x.status_code, 201)
        response = self.client.patch("api/v2/questions/1/upvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.upvoted_question)


    def test_user_upvote_question_twice(self):
        """
        test a user tries to upvote a question twice
        """
        self.token = self.login()
        y = self.client.post("api/v2/meetups",
                             data=json.dumps(self.meetup),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(y.status_code, 201)
        x = self.client.post("api/v2/meetups/1/questions",
                             data=json.dumps(self.post_question1),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(x.status_code, 201)
        self.client.patch("api/v2/questions/1/upvote",
                          headers={'x-access-token': self.token},
                          content_type="application/json")
        response = self.client.patch("api/v2/questions/1/upvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 409)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "You cannot vote twice on a single question")


    def test_downvote_question(self):
        """
        test a user can upvote a question
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.patch("api/v2/questions/1/downvote",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.downvoted_question)


    def test_wrong_response_on_vote_question(self):
        """
        test a user input a response other than upvote or downvote in the url
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.meetup),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups/1/questions",
                         data=json.dumps(self.post_question1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.patch("api/v2/questions/1/abracadabra",
                                     headers={'x-access-token': self.token},
                                     content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 400)
        self.assertEqual(result['error'], 'url vote should be upvote or downvote')


    def test_get_all_comments_on_question(self):
        """
        test a user can get all the comments posted to a question
        """
        self.token = self.login()
        a = self.client.post("api/v2/meetups",
                             data=json.dumps(self.meetup),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(a.status_code, 201)
        x = self.client.post("api/v2/meetups/1/questions",
                             data=json.dumps(self.post_question1),
                             headers={'x-access-token': self.token},
                             content_type="application/json")
        self.assertEqual(x.status_code, 201)
        y = self.client.post("api/v2/questions/1/comment",
                             headers={'x-access-token': self.token},
                             data=json.dumps(self.post_comment),
                             content_type="application/json")
        self.assertEqual(y.status_code, 201)
        response = self.client.get("api/v2/questions/1/comments",
                                   headers={'x-access-token': self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
