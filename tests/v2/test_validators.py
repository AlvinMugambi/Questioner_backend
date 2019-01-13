"""The validators and edge cases tests"""

import unittest
import json

from app import create_app
from config import app_config
from app.api.v2.models.database import init_db


class ValidatorsBaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        # Retrieve test_db url from env
        self.db_url = app_config['test_db_url']
        # initialize db, create tables
        init_db(self.db_url)

        self.user_signup = {"firstname":"star",
                            "lastname": "wars",
                            "username":"starwars",
                            "email":"galaxy@gmail.com",
                            "password": "TheRepubl1c",
                            "confirm_password":"TheRepubl1c"}

        self.user_invalid_email1 = {"firstname":"fay",
                                    "lastname": "sky",
                                    "username":"walker",
                                    "email":"faywalkergmail.com",
                                    "password": "theJed1",
                                    "confirm_password":"theJed1"}

        self.user_invalid_email2 = {"firstname":"master",
                                    "lastname": "yoda",
                                    "username":"masteryoda",
                                    "email":"jedithe@gmailcom",
                                    "password": "TheForce1",
                                    "confirm_password":"TheForce1"}

        self.password_length = {"firstname":"alvo",
                                "lastname": "nana",
                                "username":"nanaalvo",
                                "email":"jedithe@gmail.com",
                                "password": "TheF1",
                                "confirm_password":"TheF1"}

        self.password_alpha = {"firstname":"alvo",
                               "lastname": "nana",
                               "username":"nanaalvo",
                               "email":"jedis@gmail.com",
                               "password": "1224421",
                               "confirm_password":"1224421"}

        self.password_capital = {"firstname":"alvo",
                                 "lastname": "nana",
                                 "username":"nanaalvo",
                                 "email":"jedi@gmail.com",
                                 "password": "theforce1",
                                 "confirm_password":"theforce1"}

        self.password_num = {"firstname":"alvo",
                             "lastname": "nana",
                             "username":"nanaalvo",
                             "email":"jedione@gmail.com",
                             "password": "TheForce",
                             "confirm_password":"TheForce"}

    def tearDown(self):
        """
        The teardown function
        Restart the db connection and
        recreate all the tables, wiping all data
        """
        self.app.testing = False
        init_db(self.db_url)


class TestValidations(ValidatorsBaseTest):

    def test_email_already_taken(self):
        """
        Test if a user registers with an already in use Email
        """
        self.client.post("api/v2/auth/signup", data = json.dumps(self.user_signup), content_type = "application/json")
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.user_signup), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Email already taken!")

    def test_invalid_email(self):
        """
        Test user input an invalid email with no @
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.user_invalid_email1), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Invalid Email")

    def test_invalid_email_2(self):
        """
        Test user input an invalid email with no domain
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.user_invalid_email2), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Invalid Email")

    def test_pasword_length(self):
        """
        Test user input a short a password
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.password_length), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Password should not be less than 6 characters or exceed 12")

    def test_pasword_alphabets(self):
        """
        Test user input a password with no alphabets
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.password_alpha), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Password should contain a letter between a-z")

    def test_pasword_capital(self):
        """
        Test user input password has no capital letter
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.password_capital), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Password should contain a capital letter")

    def test_pasword_num(self):
        """
        Test user input password has no digits
        """
        response = self.client.post("api/v2/auth/signup", data = json.dumps(self.password_num), content_type = "application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],"Password should contain a number(0-9)")
