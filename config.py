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
    db_url = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """
    The testing configuration class
    """
    DEBUG = True
    test_db_url = os.getenv('DATABASE_TEST_URL')


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "db_url": os.getenv('DATABASE_URL'),
    "test_db_url": os.getenv('DATABASE_TEST_URL')
}
