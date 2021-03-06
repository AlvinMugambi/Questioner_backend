"""The meetups routes tests"""

import unittest
import json

# local imports
from app import create_app
from config import app_config
from app.api.v2.models.database import init_db, drop_table_if_exists

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
                             "password": "ThaOG1234",
                             "confirmpassword":"ThaOG1234"}

        self.login_admin = {"username":"iamtheadmin",
                            "password":"ThaOG1234"}

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
                             "description":"my description",
                             "meetup_date":"30/01/2900",
                             "location":"Meru",
                             "images":"me.png",
                             "tags":["trees"]
                            }

        self.post_meetup2 = {"topic":"Python",
                             "description":"my description",
                             "meetup_date":"09/01/2091",
                             "location":"Nakuru",
                             "images":"them.png",
                             "tags":["Snake"]
                            }

        self.post_meetup3 = {"toic":"Python",
                             "description":"my description",
                             "meeup_date":"3/01/2091",
                             "locaton":"Nyeri",
                             "imaes":"them.png",
                             "tgs":["Snake"]
                            }

        self.rsvp_response1 = [{"Attending": "yes",
                                "meetup": 1,
                                "topic": "Python"}]

        self.meetups_topic = {"topic":"",
                              "description":"my description",
                              "meetup_date":"30/01/2040",
                              "location":"Meru",
                              "images":"me.png",
                              "tags":["trees"]}

        self.meetups_meetup_date = {"topic":"Miraa",
                                    "description":"my description",
                                    "meetup_date":"",
                                    "location":"Meru",
                                    "images":"me.png",
                                    "tags":["trees"]}

        self.meetups_location = {"topic":"Miraa",
                                 "description":"my description",
                                 "meetup_date":"30/01/2190",
                                 "location":"",
                                 "images":"me.png",
                                 "tags":["trees"]}

        self.meetups_tags = {"topic":"Miraa",
                             "description":"my description",
                             "meetup_date":"30/01/2120",
                             "location":"Meru",
                             "images":"me.png",
                             "tags": ""}

        self.meetups_whitespace = {"topic":"     ",
                                   "description":"my description",
                                   "meetup_date":"30/01/2120",
                                   "location":"Meru",
                                   "images":"me.png",
                                   "tags": ["zcasc"]}

        self.meetups_non_alpha = {"topic":"1235454",
                                  "description":"my description",
                                  "meetup_date":"30/01/2120",
                                  "location":"Meru",
                                  "images":"me.png",
                                  "tags": ["sdvsvs"]}

        self.meetups_wrong_date = {"topic":"pythonia",
                                   "description":"my description",
                                   "meetup_date":"12142333545",
                                   "location":"Meru",
                                   "images":"me.png",
                                   "tags": ["sdvsvs"]}

        self.meetups_past_date = {"topic":"pythonia",
                                  "description":"my description",
                                  "meetup_date":"30/04/1990",
                                  "location":"Meru",
                                  "images":"me.png",
                                  "tags": ["sdvsvs"]}

        self.token = ''

    def tearDown(self):
        """
        The teardown function
        Recreate the db connection and
        recreate all the tables, wiping all data
        """
        self.app.testing = False
        drop_table_if_exists()
        # init_db(self.db_url)



class TestMeetups(MeetupsBaseTest):
    """
    The test meetups class that contains all the tests for meetups endpoints
    """

    def login(self):
        """
        Login a fake admin user
        """
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
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
        self.assertEqual(result["error"], 'tags field is required')


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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
        self.assertEqual(result["error"], 'topic field cannot be left blank')


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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
        self.assertEqual(
            result["error"], "Invalid date format. Should be DD/MM/YYYY")


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
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["status"], 422)
        self.assertEqual(result["error"], "Date should be in the future")


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
        self.assertTrue(result["data"])


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
        self.assertEqual(result['data'], {'Attendees': 0,
                                          'description': 'my description',
                                          'meetupId': 1,
                                          'topic':"Miraa",
                                          'meetupDate': "Sat, 30 Jan 2900 00:00:00 GMT",
                                          'meetupLocation':"Meru"})


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
        self.assertEqual(result["error"], "Meetup with id 10 not found")


    def test_admin_can_delete_a_meetup(self):
        """
        Test an admin user can delete a meetup
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup1),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.delete("api/v2/meetups/1",
                                      headers={'x-access-token': self.token},
                                      content_type="application/json")
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
        self.assertEqual(result["error"], "Meetup with id 10 not found")


    def test_user_can_set_rsvp_response(self):
        """
        Tests to show a user can successfully post ther attendance status
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/rsvps/yes",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['data'], self.rsvp_response1)


    def test_user_set_wrong_rsvp_response(self):
        """
        Tests to user input wrong rsvp response
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/1/rsvps/idontknow",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], 'Response should be either yes, no or maybe')


    def test_user_set_rsvp_to_unknown_meetup(self):
        """
        Tests user set attendance rsvp to a meetup not posted
        """
        self.token = self.login()
        self.client.post("api/v2/meetups",
                         data=json.dumps(self.post_meetup2),
                         headers={'x-access-token': self.token},
                         content_type="application/json")
        response = self.client.post("api/v2/meetups/2/rsvps/yes",
                                    headers={'x-access-token': self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['error'], 'Meetup with id 2 not found')
