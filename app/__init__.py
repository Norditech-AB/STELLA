import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

from app.config import flask_configs

from app.chat_queue import ChatQueue

from app.views.auth import auth_views
from app.views.chat import initiate_chat_views
from app.views.workspace import workspace_views
from app.views.agent import agent_views

# Load the environment variables from the .env file
load_dotenv()


def create_app():
    """
    Creates the Flask app and registers the blueprints.
    Loads the configuration from the config.py file.
    :return:
    """
    config_name = os.getenv('FLASK_CONFIG', 'default')

    socketio = SocketIO(ping_timeout=900, ping_interval=60)
    app = Flask(__name__)
    CORS(app, origins="*", supports_credentials=True)
    JWTManager(app)

    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode=flask_configs[config_name].ASYNC_MODE,
        logger=flask_configs[config_name].SOCKET_LOGGER,
        engineio_logger=flask_configs[config_name].ENGINEIO_LOGGER
    )

    app.config.from_object(flask_configs[config_name])
    app.extensions['socketio'] = socketio
    app.extensions['chat_queue'] = ChatQueue(num_workers=5, socketio=socketio)

    # app.register_blueprint( <blueprint> )
    app.register_blueprint(auth_views)
    app.register_blueprint(initiate_chat_views(socketio, app.extensions['chat_queue']))
    app.register_blueprint(workspace_views)
    app.register_blueprint(agent_views)

    # TODO: Debug
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"\t{rule}")

    return app, socketio
