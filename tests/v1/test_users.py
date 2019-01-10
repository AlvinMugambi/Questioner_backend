"""The user endpoints tests"""

import unittest
import json

from app import create_app

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

        self.signup_user1 = {"firstname":"alvo",
                             "lastname": "mugz",
                             "username":"alvomugz",
                             "email":"alvo@gmail.com",
                             "password": "Alvino123",
                             "confirm_password":"Alvino123"}

        self.signup_user2 = {"firstname":"Lord",
                             "lastname": "Vader",
                             "username":"Lordvader",
                             "email":"darth@gmail.com",
                             "password": "LordDarthV1",
                             "confirm_password":"Darthvader1"}

        self.signup_user3 = {"firstname":"luke",
                             "lastname": "Skywalker",
                             "username":"skywalker",
                             "email":"skywalker@gmail.com",
                             "password": "LukeSkyies1",
                             "confirm_password":"LukeSkyies1"}

        self.signup_user4 = {"firstname":"obi",
                             "lastname": "wan",
                             "username":"obiwan",
                             "email":"canobi@gmail.com",
                             "password": "ObiLight1",
                             "confirm_password":"ObiLight1"}

        self.login_user1 = {"username":"alvomugz",
                            "password":"alvino"}

        self.login_user4 = {"username":"obiwan",
                            "password":"ObiLight1"}

    def tearDown(self):
        """
        The teardown function
        """
        self.app.testing = False

class TestUserEndpoints(UserBaseTest):
    """
    The user test class that contains the test functions
    """

    def test_user_can_sign_up(self):
        """
        Test to show a user can sign up successfully
        """
        response = self.client.post("api/v1/auth/signup", data = json.dumps(self.signup_user3), content_type = "application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], 'Registered successfully!')

    def test_unmatching_passwords(self):
        """
        Test to assert that sign up passwords must match
        """
        response = self.client.post("api/v1/auth/signup", data = json.dumps(self.signup_user2), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "Passwords don't match!")

    def test_user_can_login(self):
        """
        Test to show a user can successfully login if registered
        """
        self.client.post("api/v1/auth/signup", data = json.dumps(self.signup_user4), content_type = "application/json")
        response = self.client.post("api/v1/auth/login", data = json.dumps(self.login_user4), content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], "Logged in successfully")

    def test_unregistered_user_no_login(self):
        """
        Test to show an unregistered user cannot be logged in
        """
        response = self.client.post("api/v1/auth/login", data = json.dumps(self.login_user1), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], "Register first")
