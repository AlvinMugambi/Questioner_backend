
# Questioner_backend

[![Build Status](https://travis-ci.org/AlvinMugambi/Questioner_backend.svg?branch=develop)](https://travis-ci.org/AlvinMugambi/Questioner_backend)[![Maintainability](https://api.codeclimate.com/v1/badges/c4e627cf1f50880cb8fb/maintainability)](https://codeclimate.com/github/AlvinMugambi/Questioner_backend/maintainability)[![Coverage Status](https://coveralls.io/repos/github/AlvinMugambi/Questioner_backend/badge.svg?branch=ft-api-get-all-meetups-%23163033399)](https://coveralls.io/github/AlvinMugambi/Questioner_backend?branch=ft-api-get-all-meetups-%23163033399)


Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered.

The project is managed using [Pivotal Tracker](https://www.pivotaltracker.com). You can view the board https://www.pivotaltracker.com/n/projects/2235202.

The repo for the frontend is available at https://github.com/AlvinMugambi/Questioner

## Deployment
Website is hosted on [Questioner](https://alvinmugambi.github.io/Questioner/UI/templates/homepage.html)

Project API demo is hosted on [Heroku](https://the-questioner-backend.herokuapp.com)

## Prerequisites

- [Atom](https://atom.io/)
- [Python 3.6](https://www.python.org)
- [Insomnia](https://insomnia.rest) / [Postman](https://www.getpostman.com)

## Installation

- Clone the repo
```
$ git clone
```

- CD into the folder
```
$ cd Questioner_backend
```

- Create a virtual environment
```
$ python3 -m venv env
```

- Activate the virtual environment
```
$ source env/bin/activate
```

- Install dependencies
```
$ pip install -r requirements.txt
```

- Set the environment variables
```
$ mv .env.example .env
$ source .env
```

- Run the app
```
$ python run.py or flask run
```

- Testing
```
$ pytest --cov=app
```

## API Endpoints (V1)

| **HTTP METHOD** | **URI ** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v1/auth/login` | Login |
| **POST** | `/api/v1/auth/Sign Up` | Sign Up |
| **POST** | `/api/v1/meetups` | Create a meetup |
| **DELETE** | `/api/v1/meetups/<int:meetup_id>` | Delete a meetup |
| **POST** | `/api/v1/questions` | Post a question to a specific meetup |
| **GET** | `/api/v1/meetups/<int:meet_id>/questions` | Get all questions on a meetup |
| **POST** | `/api/v1/questions/<int:question_id>/comment` | Comment on a question |
| **GET** | `/api/v1/meetups/upcoming` | Fetch all upcoming meetups |
| **GET** | `/api/v1/meetups/<int:meetup_id>` | Fetch a specific meetup |
| **POST** | `/api/v1/meetups/<int:meetup_id>/rsvps/<resp>` | RSVP to a meetup |
| **PATCH** | `/api/v1/questions/<int:question_id>/upvote` | Upvote a question |
| **PATCH** | `/api/v1/questions/<int:question_id>/downvote` | Downvote a question |

## Author

Alvin Mugambi - [Alv0](https://github.com/AlvinMugambi)
