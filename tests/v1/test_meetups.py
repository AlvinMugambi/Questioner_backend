"""The meetups tests"""

import os
import unittest
import json

# local imports
from app import create_app

class MeetupsBaseTest(unittest.TestCase):

    """
    The meetups base test that contains the setUp funcion that occurs before each test
    """

    def setUp(self):

        self.app = create_app("testing")
        self.client = self.app.test_client()

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

        self.meetups = [{"created_at": "Wed, 09 Jan 2019 01:30:13 GMT",
                         "id": 1,
                         "images": ["me.png",
                                    "you.png"],
                         "location": "Meru",
                         "meetup_date": "30/01/1990",
                         "tags": ["trees",
                                  "vegetation"],
                         "topic": "Miraa"},
                        {"created_at": "Wed, 09 Jan 2019 01:30:34 GMT",
                         "id": 2,
                         "images": ["them.png",
                                    "they.png"],
                         "location": "Nyeri",
                         "meetup_date": "3/01/1991",
                         "tags": ["Snake", "Camel"],
                         "topic": "Python"
                        }]



class TestMeetups(MeetupsBaseTest):
    """
    The test meetups class that contains all the tests for meetups endpoints
    """

    def test_user_can_create_a_meetup(self):
        """
        Test that a user can enter meetup details and create a meetup
        """

        response = self.client.post("api/v1/meetups", data = json.dumps(self.post_meetup1), content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], 201)
        self.assertEqual(result["data"], [{"location": "Meru", "meetup_date": "30/01/1990", "tags": ["trees", "vegetation"], "topic": "Miraa"}])


    def test_user_can_get_all_meetups(self):
        """
        Tests to show that a user can successfully get all meetups
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.post_meetup1), content_type = "application/json")
        self.client.post("api/v1/meetups", data = json.dumps(self.post_meetup2),  content_type = "application/json")

        response = self.client.get("api/v1/meetups", content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["status"], 200)
        # self.assertEqual(result["data"], self.meetups)

    def test_user_can_get_a_specific_meetup(self):
        """
        Test to show that a user can successfully get a specific meetup using a metup id
        """
        self.client.post("api/v1/meetups", data = json.dumps(self.post_meetup1), content_type = "application/json")
        self.client.post("api/v1/meetups", data = json.dumps(self.post_meetup2),  content_type = "application/json")

        response = self.client.get("api/v1/meetups/1", content_type = "application/json")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data'], [{"id" : 1,
                                           "topic":"Miraa",
                                           "location" : "Meru",
                                           "meetup_date":"30/01/1990",
                                           "tags" :["trees", "vegetation"]}])
