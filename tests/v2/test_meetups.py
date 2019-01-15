
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

        self.signup_admin = {"username":"iamtheadmin",
                             "email":"mastryoda@gmail.com",
                             "password": "NumberFrce1",
                             "confirm_password":"NumberFrce1"}

        self.login_admin = {"username":"iamtheadmin",
                            "password":"NumberFrce1"}

        self.signup_user2 = {"username":"fakestyoda",
                             "email":"yodason@gmail.com",
                             "password":"Obi1ight1",
                             "confirm_password":"Obi1ight1"}

        self.login_user2 = {"username":"fakestyoda",
                            "password":"Obi1ight1"}

        self.post_meetup1 = {"topic":"Miraa",
                             "meetup_date":"30/01/1990",
                             "location":"Meru",
                             "images":["me.png", "you.png"],
                             "tags":["trees", "vegetation"]
                            }

        self.post_meetup2 = {"topic":"Python",
                             "meetup_date":"3/01/1991",
                             "location":"Nyeri",
                             "images":["them.png", "they.png"],
                             "tags":["Snake", "Camel"]
                            }
        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Miraa"}]

        self.meetups_topic = {"topic":"",
                              "meetup_date":"30/01/1990",
                              "location":"Meru",
                              "images":["me.png", "you.png"],
                              "tags":["trees", "vegetation"]}

        self.meetups_meetup_date = {"topic":"Miraa",
                                    "meetup_date":"",
                                    "location":"Meru",
                                    "images":["me.png", "you.png"],
                                    "tags":["trees", "vegetation"]}

        self.meetups_location = {"topic":"Miraa",
                                 "meetup_date":"30/01/1990",
                                 "location":"",
                                 "images":["me.png", "you.png"],
                                 "tags":["trees", "vegetation"]}

        self.meetups_tags = {"topic":"Miraa",
                             "meetup_date":"30/01/1990",
                             "location":"Meru",
                             "images":["me.png", "you.png"],
                             "tags":[]}

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
        self.client.post(
            'api/v2/auth/signup', data=json.dumps(self.signup_admin), content_type="application/json")
        login = self.client.post(
            'api/v2/auth/login', data=json.dumps(self.login_admin), content_type="application/json")
        data = json.loads(login.data.decode('utf-8'))
        self.token = data["token"]
        return self.token


    def test_no_topic_data(self):
        """
        Test if no topic data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetups_topic),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'topic field is required')

    def test_no_meetup_date_data(self):
        """
        Test if no meetup date data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetups_meetup_date),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'meetup_date field is required')

    def test_no_tags_data(self):
        """
        Test if no tags data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetups_tags),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'tags field is required')

    def test_no_location_data(self):
        """
        Test if no location data provided
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.meetups_location),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["status"], 400)
        self.assertEqual(result["error"], 'location field is required')

    def test_an_admin_user_can_create_a_meetup(self):
        """
        Test that an admin user can enter meetup details and create a meetup
        """
        self.token = self.login()
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': self.token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"],
                        [{"location": "Meru", "meetup_date": "30/01/1990", "tags": ["trees", "vegetation"], "topic": "Miraa"}])


    def test_a_regular_user_cannot_create_a_meetup(self):
        """
        Test that a regular user cannot create a meetup
        """
        self.client.post("api/v2/auth/signup",
                         data = json.dumps(self.signup_user2),
                         content_type = "application/json")
        login = self.client.post("api/v2/auth/login",
                                 data = json.dumps(self.login_user2),
                                 content_type = "application/json")
        resp = json.loads(login.data.decode('utf-8'))
        user_token =resp['token']
        response = self.client.post("api/v2/meetups",
                                    data = json.dumps(self.post_meetup1),
                                    headers={'x-access-token': user_token},
                                    content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["status"], 401)
        self.assertEqual(result["error"], "You are not allowed to perfom this function")

    # def test_admin_can_delete_a_meetup(self):
    #     """
    #     Test an admin user can delete a meetup
    #     """
    #     self.token = self.login()
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup1), headers={'x-access-token': self.token}, content_type = "application/json")
    #     response = self.client.delete("api/v2/meetups/1", headers={'x-access-token': self.token}, content_type = "application/json")
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(result["status"], 200)
    #     self.assertEqual(result["data"], "Deleted successfully")

    # def test_meetup_not_found(self):
    #     """
    #     Test response when a meetup is not found
    #     """
    #     self.token = self.login()
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup1), headers={'x-access-token': self.token}, content_type = "application/json")
    #     response = self.client.delete("api/v2/meetups/10", headers={'x-access-token': self.token}, content_type = "application/json")
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(result["status"], 404)
    #     self.assertEqual(result["data"], "Meetup with id 10 not found")


    # def test_user_can_get_all_meetups(self):
    #     """
    #     Tests to show that a user can successfully get all meetups
    #     """
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup1), headers={'x-access-token': self.token}, content_type = "application/json")
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup2),  headers={'x-access-token': self.token}, content_type = "application/json")
    #
    #     response = self.client.get("api/v2/meetups/upcoming", content_type = "application/json")
    #     self.assertEqual(response.status_code, 200)
    #
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(result["status"], 200)
    #     self.assertTrue(result["data"])
    #
    #
    # def test_user_can_get_a_specific_meetup(self):
    #     """
    #     Test to show that a user can successfully get a specific meetup using a metup id
    #     """
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup1), headers={'x-access-token': self.token}, content_type = "application/json")
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup2),  headers={'x-access-token': self.token}, content_type = "application/json")
    #
    #     response = self.client.get("api/v2/meetups/1", content_type = "application/json")
    #     self.assertEqual(response.status_code, 200)
    #
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(result['status'], 200)
    #     self.assertEqual(result['data'], [{"id": 1,
    #                                        "location": "Meru",
    #                                        "meetup_date": "30/01/1990",
    #                                        "tags": ["trees", "vegetation"],
    #                                        "topic": "Miraa"}])
    #
    # def test_user_can_set_rsvp_response(self):
    #     """
    #     Tests to show a user can successfully post ther attendance status
    #     """
    #     self.client.post("api/v2/meetups", data = json.dumps(self.post_meetup2),  headers={'x-access-token': self.token}, content_type = "application/json")
    #     response = self.client.post("api/v2/meetups/1/rsvps/yes", content_type = "application/json")
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(result['data'], self.rsvp_response1)
