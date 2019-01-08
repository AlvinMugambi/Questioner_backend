"""The meetups tests"""

import unittest
import json

# local imports
from app import create_app

class MeetupsBaseTest(unittest.TestCase):

    """The meetups base test that contains the setUp funcion that occurs before each test"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.post_meetup = {"topic":"Miraa",
                            "meetup_date":"30/01/1990",
                            "location":"Meru",
                            "images":["me.png", "you.png"],
                            "tags":["trees", "vegetation"]
                           }


class TestMeetups(MeetupsBaseTest):
    """ The test meetups class that contains all the tests for meetups endpoints"""

    def test_user_can_post_question(self):

        """ Test that a user can enter meetup details and create a meetup"""

        response = self.client.post("api/v1/meetups",data = json.dumps(self.post_meetup), content_type = "application/json")
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["data"], [{"topic" :"Miraa",
                                           "location" :"Meru",
                                           "meetup_date" :"30/01/1990",
                                           "tags" : ["trees", "vegetation",]}])


if __name__ == '__main__':
    unittest.main()
