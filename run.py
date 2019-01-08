
import os

from dotenv import load_dotenv

from app import create_app

APP_ENV = os.getenv("APP_ENV")
app = create_app(APP_ENV)


if __name__ == '__main__':
    app.run(debug=True)
