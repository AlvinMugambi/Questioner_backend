"""
The meetups models
"""

from datetime import datetime

MEETUPS = []


class Meetup:
    """
    The Meetup class that contains the meetup models
    """
    def __init__(self, topic, meetup_date, location, images, tags):
        """
        The initialization of the Meetup class that defines its variables
        """
        self.id = len(MEETUPS)+1
        self.topic = topic
        self.meetup_date = meetup_date
        self.location = location
        self.images = images
        self.tags = tags
        self.created_at = datetime.now()

    def save_meetup(self):
        """
        saves new meetup to store
        """
        MEETUPS.append(self)

    @staticmethod
    def get_all_meetups():
        """
        gets all meetups
        """
        return [Meetup.to_json(meetup) for meetup in MEETUPS]


    @staticmethod
    def to_json(meetup):
        """
        format meetup object to a readable dictionary
        """
        return {
            "id": meetup.id,
            "topic": meetup.topic,
            "meetup_date": meetup.meetup_date,
            "location": meetup.location,
            "images": meetup.images,
            "tags": meetup.tags,
            "created_at": meetup.created_at
        }
