"""The meetups routes tests"""

import unittest
import json

# local imports
from app import create_app
from config import app_config
from app.api.v2.models.database import init_db

class MeetupsBaseTest(unittest.TestCase):

    """
    The meetups base test that contains the setUp funcion that occurs before each test
    """

    def setUp(self):

        self.app = create_app("testing")
        self.client = self.app.test_client()
        # Retrieve test_db url from env
        self.db_url = app_config['test_db_url']
        # initialize db, create tables
        init_db(self.db_url)

        self.signup_admin = {"firstname":"the",
                             "lastname":"admin",
                             "phoneNumber":"0712345678",
                             "username":"iamtheadmin",
                             "email":"mastryoda@gmail.com",
                             "password": "NumberFrce1",
                             "confirmpassword":"NumberFrce1"}

        self.login_admin = {"username":"iamtheadmin",
                            "password":"NumberFrce1"}

        self.signup_user2 = {"firstname":"iam",
                             "lastname":"yoda",
                             "phoneNumber":"0702345678",
                             "username":"fakestyoda",
                             "email":"yodason@gmail.com",
                             "password":"Obi1ight1",
                             "confirmpassword":"Obi1ight1"}

        self.login_user2 = {"username":"fakestyoda",
                            "password":"Obi1ight1"}

        self.post_meetup1 = {"topic":"Miraa",
                             "meetup_date":"30/01/2900",
                             "location":"Meru",
                             "images":"me.png",
                             "tags":"trees"
                            }

        self.post_meetup2 = {"topic":"Python",
                             "meetup_date":"3/01/2091",
                             "location":"Nyeri",
                             "images":"them.png",
                             "tags":"Snake"
                            }

        self.post_meetup3 = {"toic":"Python",
                             "meeup_date":"3/01/2091",
                             "locaton":"Nyeri",
                             "imaes":"them.png",
                             "tgs":"Snake"
                            }

        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Miraa"}]

        self.meetups_topic = {"topic":"",
                              "meetup_date":"30/01/2040",
                              "location":"Meru",
                              "images":"me.png",
                              "tags":"trees"}

        self.meetups_meetup_date = {"topic":"Miraa",
                                    "meetup_date":"",
                                    "location":"Meru",
                                    "images":"me.png",
                                    "tags":"trees"}

        self.meetups_location = {"topic":"Miraa",
                                 "meetup_date":"30/01/2190",
                                 "location":"",
                                 "images":"me.png",
                                 "tags":"trees"}

        self.meetups_tags = {"topic":"Miraa",
                             "meetup_date":"30/01/2120",
                             "location":"Meru",
                             "images":"me.png",
                             "tags": ""}

        self.meetups_whitespace = {"topic":"     ",
                                   "meetup_date":"30/01/2120",
                                   "location":"Meru",
                                   "images":"me.png",
                                   "tags": "zcasc"}

        self.meetups_non_alpha = {"topic":"1235454",
                                  "meetup_date":"30/01/2120",
                                  "location":"Meru",
                                  "images":"me.png",
                                  "tags": "sdvsvs"}

        self.meetups_wrong_date = {"topic":"pythonia",
                                   "meetup_date":"12142333545",
                                   "location":"Meru",
                                   "images":"me.png",
                                   "tags": "sdvsvs"}

        self.meetups_past_date = {"topic":"pythonia",
                                  "meetup_date":"30/04/1990",
                                  "location":"Meru",
                                  "images":"me.png",
                                  "tags": "sdvsvs"}

        self.token = ''

    def tearDown(self):
        """
        The teardown function
        Recreate the db connection and
        recreate all the tables, wiping all data
        """
        self.app.testing = False
        init_db(self.db_url)



class TestMeetups(MeetupsBaseTest):
    """
    The test meetups class that contains all the tests for meetups endpoints
    """

    def login(self):
        """
        Login a fake admin user
        """
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(self.signup_admin),
                         content_type="application/json")
        login = self.client.post('api/v2/auth/login',
                                 data=json.dumps(self.login_admin),
                                 content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token


    def test_no_topic_data(self):
        """
        Test if no topic data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_topic),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'topic field cannot be left blank')


    def test_no_meetup_date_data(self):
        """
        Test if no meetup date data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_meetup_date),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'meetup_date field cannot be left blank')


    def test_no_tags_data(self):
        """
        Test if no tags data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_tags),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'tags field cannot be left blank')


    def test_no_location_data(self):
        """
        Test if no location data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_location),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'location field cannot be left blank')


    def test_wrong_json_keys(self):
        """
        Test that an admin user enters the wrong keys
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup3),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["error"], 'Should be topic, meetup_date, location, images and tags')


    def test_user_input_whitespace(self):
        """
        Test if only whitespace provided on input
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_whitespace),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'topic field cannot be left blank')


    def test_user_input_non_alpha(self):
        """
        Test if user input digits or non alphabet characters in string fields
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_non_alpha),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["Error"], 'Make sure you only use letters in your topic')


    def test_user_input_invalid_date(self):
        """
        Test if user input an invalid date or format
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_wrong_date),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(
            result["Error"], "Invalid date format. Should be DD/MM/YYYY")


    def test_user_input_past_date(self):
        """
        Test if user input a date that is in the past
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.meetups_past_date),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["Error"], "Date should be in the future")


    def test_an_admin_user_can_create_a_meetup(self):
        """
        Test that an admin user can enter meetup details and create a meetup
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup1),
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(
            result["data"],
            [{"location": "Meru", "meetup_date": "30 Jan 2900", "tags": "trees", "topic": "Miraa"}])


    def test_a_regular_user_cannot_create_a_meetup(self):
        """
        Test that a regular user cannot create a meetup
        """
        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.signup_user2),
                         content_type="application/json")
        login = self.client.post("api/v2/auth/login",
                                 data=json.dumps(self.login_user2),
                                 content_type="application/json")
        resp = json.loads(login.data.decode('utf-8'))
        user_token = resp['token']
        response = self.client.post("api/v2/meetups",
                                    data=json.dumps(self.post_meetup1),
                                    headers={'x-access-token': user_token},
                                    content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(
            result["error"], "You are not allowed to perfom this function")


    def test_user_can_get_a_specific_meetup(self):
        """
        Test to show that a user can successfully get a specific meetup using a meetup id
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v2/meetups/1",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data'], [[1,
                                           "Miraa",
                                           "30 Jan 2900",
                                           "Meru"]])


    def test_user_can_get_all_meetups(self):
        """
        Tests to show that a user can successfully get all meetups
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")

        response = self.client.get("api/v2/meetups/upcoming",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 200)
        self.assertTrue(result["data"])


    def test_user_cannot_get_all_meetups_if_no_meetup_posted(self):
        """
        Tests to show that a user cannot get all meetups when there is no meetup posted
        """
        response = self.client.get("api/v2/meetups/upcoming",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 404)
        self.assertEqual(
            result["data"], "Currently there are no meetups scheduled.")


    def test_meetup_not_found(self):
        """
        Test response when a meetup is not found
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.get("api/v2/meetups/10",
                                   headers={'x-access-token': self.token},
                                   content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)
        self.assertEqual(result["data"], "Meetup with id 10 not found")


    def test_admin_can_delete_a_meetup(self):
        """
        Test an admin user can delete a meetup
        """
        self.token = self.login()
        self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup1), headers={'x-access-token': self.token}, content_type = "application/json")
        response = self.client.delete("api/v2/meetups/1", headers={'x-access-token': self.token}, content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["data"], "Deleted successfully")

    def test_admin_cannot_delete_a_meetup_not_posted(self):
        """
        Test response when an admin tries to delete a meetup thats not posted
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.delete("api/v2/meetups/10",
                                      headers={'x-access-token': self.token},
                                      content_type="application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result["status"], 404)
        self.assertEqual(result["data"], "Meetup with id 10 not found")


    # def test_user_can_set_rsvp_response(self):
    #     """
    #     Tests to show a user can successfully post ther attendance status
    #     """
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup2),  headers={'x-access-token': self.token}, content_type = "application/json")
    #     response = self.client.post("api/v2/meetups/1/rsvps/yes", content_type = "application/json")
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(result['data'], self.rsvp_response1)
