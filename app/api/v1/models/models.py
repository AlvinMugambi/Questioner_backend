from datetime import datetime


meetups = []

class Meetup():

    def __init__(self, id, topic, meetup_date, location, images, tags):
        self.id = len(meetups)+1
        self.topic = topic
        self.meetup_date = meetup_date
        self.location = location
        self.images = images
        self.tags = tags
        self.created_at = datetime.now()
