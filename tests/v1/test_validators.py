import unittest
import json

from app import create_app


class ValidatorsBaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user_signup = {"firstname":"star",
                            "lastname": "wars",
                            "username":"starwars",
                            "email":"galaxy@gmail.com",
                            "password": "TheRepubl1c",
                            "confirm_password":"TheRepubl1c"}

        self.user_login = {"username":"starwars",
                           "password": "TheRepubl1",
                           "confirm_password":"TheRepubl1"}

        self.user_signup1 = {"firstname":"hans",
                             "lastname": "olo",
                             "username":"pilot",
                             "email":"thefly@gmail.com",
                             "password": "Chewbacca1",
                             "confirm_password":"Chewbacca1"}

        self.user_login1 = {"username":"piloti",
                            "password": "Chewbacca1",
                            "confirm_password":"Chewbacca1"}

        self.user_signup2 = {"firstname":"    ",
                             "lastname": "wars",
                             "username":"stars",
                             "email":"galaxies@gmail.com",
                             "password": "TheRepubl1cs",
                             "confirm_password":"TheRepubl1cs"}

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
        self.app.testing = False


class TestValidations(ValidatorsBaseTest):

    def test_email_already_taken(self):
        """
        Test an email is already in use
        """
        self.client.post("api/v1/auth/signup",
                         data=json.dumps(self.user_signup),
                         content_type="application/json")
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.user_signup),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Email already taken!")

    def test_invalid_email(self):
        """
        Test an email has no @
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.user_invalid_email1),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Invalid Email")

    def test_invalid_email_2(self):
        """
        Test an email has no .com
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.user_invalid_email2),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Invalid Email")

    def test_pasword_length(self):
        """
        Test an password is too short
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.password_length),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'],
                         "Password should not be less than 6 characters or exceed 12")

    def test_pasword_alphabets(self):
        """
        Test an password has no alphabets
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.password_alpha),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a letter between a-z")

    def test_pasword_capital(self):
        """
        Test an password has no capital letter
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.password_capital),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a capital letter")

    def test_pasword_num(self):
        """
        Test an password has no digits
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.password_num),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Password should contain a number(0-9)")

    def test_user_login_wrong_password(self):
        """
        Test an user input correct username but wrong password
        """
        self.client.post("api/v1/auth/signup",
                         data=json.dumps(self.user_signup),
                         content_type="application/json")
        response = self.client.post("api/v1/auth/login",
                                    data=json.dumps(self.user_login),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "Wrong password")
        self.assertEqual(result['status'], 400)

    def test_user_login_wrong_username(self):
        """
        Test an user input correct password but wrong username
        """
        self.client.post("api/v1/auth/signup",
                         data=json.dumps(self.user_signup1),
                         content_type="application/json")
        response = self.client.post("api/v1/auth/login",
                                    data=json.dumps(self.user_login1),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "The username is incorrect")
        self.assertEqual(result['status'], 400)


    def test_user_login_input_whitespace(self):
        """
        Test an user input whitespace at data request
        """
        response = self.client.post("api/v1/auth/signup",
                                    data=json.dumps(self.user_signup2),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], "firstname field cannot be left blank")
        self.assertEqual(result['status'], 400)
