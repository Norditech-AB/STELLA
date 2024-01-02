import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class FlaskConfig:
    ASYNC_MODE = os.getenv("ASYNC_MODE")
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    SOCK_SERVER_OPTIONS = {'ping_interval': int(os.getenv("SOCK_SERVER_OPTIONS_PING_INTERVAL"))}


class DevelopmentConfig(FlaskConfig):
    DEBUG = True
    SOCKET_LOGGER = True
    ENGINEIO_LOGGER = True


class ProductionConfig(FlaskConfig):
    DEBUG = False
    SOCKET_LOGGER = False
    ENGINEIO_LOGGER = False


flask_configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
