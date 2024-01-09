import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class FlaskConfig:
    try:
        ASYNC_MODE = os.getenv("ASYNC_MODE")
        CORS_HEADERS = 'Content-Type'
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", None)))
        SOCK_SERVER_OPTIONS = {'ping_interval': int(os.getenv("SOCK_SERVER_OPTIONS_PING_INTERVAL"))}

    except Exception as e:
        print(f"There was an error creating the STELLA application. ({e})")
        print("Please validate your configuration and try again.")
        print(" - tip: run `stella configure` to configure your application.")
        exit(1)


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
