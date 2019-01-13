"""
The app configurations
"""
import os

class Config:
    """
    The default configuration class
    """
    DEBUG = False


class DevelopmentConfig(Config):
    """
    The development configuration class
    """
    DEBUG = True


class TestingConfig(Config):
    """
    The testing configuration class
    """
    DEBUG = True


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "db_url": os.getenv('DATABASE_URL')
}
