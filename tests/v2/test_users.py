"""The user endpoints tests"""

import unittest
import json

from app import create_app
from config import app_config
from app.api.v2.models.database import init_db

class UserBaseTest(unittest.TestCase):
    """
    The base class for seeting up the user tests and tearing down
    """

    def setUp(self):
        """
        set the variables before each test
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        # Retrieve test_db url from env
        self.db_url = app_config['test_db_url']
        # initialize db, create tables
        init_db(self.db_url)

        self.signup_user1 = {"username":"alvomugz",
                             "email":"alvo@gmail.com",
                             "password": "Alvino123",
                             "confirm_password":"Alvino123"}

        self.signup_user2 = {"username":"Lordvader",
                             "email":"darth@gmail.com",
                             "password": "LordDarthV1",
                             "confirm_password":"Darthvader1"}

        self.signup_user3 = {"username":"skywalker",
                             "email":"skywalker@gmail.com",
                             "password": "LukeSkyies1",
                             "confirm_password":"LukeSkyies1"}

        self.signup_user4 = {"username":"mrcanobi",
                             "email":"canobi@gmail.com",
                             "password": "ObiLight1",
                             "confirm_password":"ObiLight1"}

        self.signup_user5 = {"username":"kyloRen",
                             "email":"newdarth@gmail.com",
                             "password": "kyloRen1",
                             "confirm_password":"kyloRen1"}

        self.signup_user6 = {"name":"chwebacca",
                             "emal":"chewie@gmail.com",
                             "passrd": "chewie123",
                             "confirm_assword":"chewie123"}

        self.login_user1 = {"username":"alvomugz",
                            "password":"alvino"}

        self.login_user4 = {"username":"mrcanobi",
                            "password":"ObiLight1"}

        self.login_user5 = {"username":"kyloRen",
                            "password":"kyloRen1"}

        self.login_user6 = {"username":"kyloRen",
                            "password":"kyloRen"}

    def tearDown(self):
        """
        The teardown function
        Recreate the db connection and
        recreate all the tables, wiping all data
        """
        self.app.testing = False
        init_db(self.db_url)

class TestUserEndpoints(UserBaseTest):
    """
    The user test class that contains the test functions
    """

    def test_user_wrong_json_keys(self):
        """
        Test to show a user can sign up successfully
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user6), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], 'Check your json keys')

    def test_user_can_sign_up(self):
        """
        Test to show a user can sign up successfully
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user1), content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], 'Registered successfully!')

    def test_unmatching_passwords(self):
        """
        Test to assert that sign up passwords must match
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user2), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "Passwords don't match!")

    def test_user_can_login(self):
        """
        Test to show a user can successfully login if registered
        """
        self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user5), content_type = "application/json")
        response = self.client.post("api/v2/auth/login", data = json.dumps(self.login_user5), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertTrue(result['token'])
        self.assertEqual(result["message"], "Logged in successfully")

    def test_unregistered_user_no_login(self):
        """
        Test to show an unregistered user cannot be logged in
        """
        response = self.client.post("api/v2/auth/login", data = json.dumps(self.login_user1), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], "The username or passsword is incorrect")

    def test_user_login_wrong_password(self):
        """
        Test to show a user can successfully login if registered
        """
        self.client.post("api/v2/auth/signup", data = json.dumps(self.signup_user5), content_type = "application/json")
        response = self.client.post("api/v2/auth/login", data = json.dumps(self.login_user6), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "wrong password")
