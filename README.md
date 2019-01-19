
# Questioner_backend

[![Build Status](https://travis-ci.org/AlvinMugambi/Questioner_backend.svg?branch=develop)](https://travis-ci.org/AlvinMugambi/Questioner_backend)[![Maintainability](https://api.codeclimate.com/v1/badges/c4e627cf1f50880cb8fb/maintainability)](https://codeclimate.com/github/AlvinMugambi/Questioner_backend/maintainability)[![Coverage Status](https://coveralls.io/repos/github/AlvinMugambi/Questioner_backend/badge.svg?branch=develop)](https://coveralls.io/github/AlvinMugambi/Questioner_backend?branch=develop)

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered.

The project is managed using [Pivotal Tracker](https://www.pivotaltracker.com). You can view the board https://www.pivotaltracker.com/n/projects/2235202.

The repo for the frontend is available at https://github.com/AlvinMugambi/Questioner

## Deployment
Website is hosted on [Questioner](https://alvinmugambi.github.io/Questioner/UI/templates/homepage.html)

API Documentation https://documenter.getpostman.com/view/6135035/RznLGw8a

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

- Install postgres
```
$ sudo apt install postgresql postgresql-contrib (ubuntu)
```

- Create database
```
$ createdb Questioner_db
$ createdb Questioner_test_db
```

- Set the environment variables
```
$ Set database URIs in the .env_sample
$ source .env_sample
```

- Run the app
```
$ python run.py or flask run
```

- Testing
```
$ pytest --cov=app
```

## API Endpoints (V2)

| **HTTP METHOD** | **URI ** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/auth/login` | Login |
| **POST** | `/api/v2/auth/Signup` | Sign Up |
| **POST** | `/api/v2/auth/logout` | Logout |
| **GET** | `/api/v2/profile` | User Profile |
| **POST** | `/api/v2/meetups` | Create a meetup |
| **DELETE** | `/api/v2/meetups/<int:meetup_id>` | Delete a meetup |
| **POST** | `/api/v2/questions` | Post a question to a specific meetup |
| **GET** | `/api/v2/meetups/<int:meet_id>/questions` | Get all questions on a meetup |
| **POST** | `/api/v2/questions/<int:question_id>/comment` | Comment on a question |
| **GET** | `/api/v2/questions/<int:question_id>/comments` | Get all comments on a question |
| **GET** | `/api/v2/meetups/upcoming` | Fetch all upcoming meetups |
| **GET** | `/api/v2/meetups/<int:meetup_id>` | Fetch a specific meetup |
| **POST** | `/api/v2/meetups/<int:meetup_id>/rsvps/<resp>` | RSVP to a meetup |
| **PATCH** | `/api/v2/questions/<int:question_id>/upvote` | Upvote a question |
| **PATCH** | `/api/v2/questions/<int:question_id>/downvote` | Downvote a question |

## Author

Alvin Mugambi - [Alv0](https://github.com/AlvinMugambi)
