"""
The app configurations
"""

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
    "testing": TestingConfig
}
