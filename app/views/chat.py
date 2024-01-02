import json
import time

from uuid import uuid4

from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import join_room, leave_room

from app.db import db
from app.models.chat import Chat


def initiate_chat_views(socketio, chat_queue):
    chat_views = Blueprint('chat_views', __name__)

    @chat_views.route('/chat/authorize', methods=['GET'])
    @jwt_required()
    def authorize_chat():
        """
        Returns a connection string for the user to connect with.
        :return:
        """
        user_id = get_jwt_identity()

        # Get chat id from url param
        chat_id = request.args.get('chat_id')

        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 404

        # Check if user is the owner of the chat
        if chat.owner != user_id:
            return jsonify({"msg": "User is not the owner of the chat"}), 401

        connection_string = db.create_chat_connection_string(
            chat_id=chat_id,
            string=str(uuid4()),
            created_at=time.time(),
            expires_at=time.time() + 60 * 5,  # 5 minutes expiration time
            created_by=user_id
        )

        return jsonify(connection_string.to_dict()), 200

    @chat_views.route('/chat/authorize/message', methods=['GET'])
    @jwt_required()
    def authorize_chat_message():
        """
        Returns a secret that must be passed when the user sends a message through SocketIO.
        :return:
        """
        user_id = get_jwt_identity()
        chat_id = request.args.get('chat_id')

        # Check if chat exists
        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 404

        # Check if user is the owner of the chat
        if chat.owner != user_id:
            return jsonify({"msg": "User is not the owner of the chat"}), 401

        message_string = db.create_chat_message_string(
            chat_id=chat_id,
            string=str(uuid4()),
            created_at=time.time(),
            expires_at=time.time() + 60 * 1,  # 1 minute expiration time
            created_by=user_id
        )

        return jsonify(message_string.to_dict()), 200

    @chat_views.route('/chat', methods=['POST'])
    @jwt_required()
    def create_chat():
        user_id = get_jwt_identity()
        # Get workspace id from url param
        workspace_id = request.args.get('workspace_id')
        if not workspace_id:
            return jsonify({"msg": "Missing workspace id"}), 400

        # Check if workspace exists
        try:
            workspace = db.get_workspace(workspace_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 404

        # Check if user is the owner of the workspace
        if workspace.owner != user_id:
            print(workspace.owner, user_id)
            return jsonify({"msg": "User is not the owner of the workspace"}), 401

        # Create chat
        chat = db.create_chat(
            workspace_id=workspace_id,
            user_id=user_id
        )

        return jsonify({"msg": "Chat created successfully", "chat": chat.to_dict(), "workspace": workspace.to_dict()}), 200

    @chat_views.route('/chat', methods=['GET'])
    @jwt_required()
    def get_chat():
        user_id = get_jwt_identity()

        # Get chat id from url param
        chat_id = request.args.get('chat_id')

        # Check if chat exists
        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 404

        # Check if user is the owner of the chat
        if chat.owner != chat_id:
            return jsonify({"msg": "User is not the owner of the chat"}), 401

        return jsonify(chat.to_dict()), 200

    @chat_views.route('/chat', methods=['DELETE'])
    @jwt_required()
    def delete_chat():
        identity = get_jwt_identity()

        # Get chat id from url param
        chat_id = request.args.get('chat_id')

        # Check if chat exists
        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 404

        # Check if user is the owner of the chat
        if chat.owner != identity:
            return jsonify({"msg": "User is not the owner of the chat"}), 401

        # Delete chat
        try:
            db.delete_chat(chat_id)
        except Exception as e:
            return jsonify({"msg": str(e)}), 500

        return jsonify({"msg": "Chat deleted successfully"}), 200

    @socketio.on('connect', namespace='/chat')
    def connect_to_chat():
        """
        Connects the user to a chat. Uses the connection string to verify that the user is allowed to connect.
        :return:
        """
        chat_id = request.args.get('chat_id')
        connection_string = request.args.get('connection_string')

        if not chat_id:
            print("Missing chat id")
            return
        if not connection_string:
            print("Missing connection string")
            return

        # Check if connection string exists
        try:
            db_connection_string = db.get_chat_connection_string(connection_string)
        except Exception as e:
            print(str(e))
            return

        # Check if connection string is expired
        if db_connection_string.expires_at < time.time():
            print("Connection string expired")
            # Invalidate connection string
            try:
                db.delete_chat_connection_string(connection_string)
            except Exception as e:
                print(str(e))
            return

        # Check if connection string is for the correct chat
        if db_connection_string.chat_id != chat_id:
            print("Connection string is for the wrong chat")
            return

        # Check if chat exists
        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            print(str(e))
            return

        # Get the workspace id from chat
        workspace_id = chat.workspace_id

        # Check if workspace exists
        try:
            workspace = db.get_workspace(workspace_id)
        except Exception as e:
            print(str(e))
            return

        # Set the last_chat_id in the workspace
        workspace.last_chat_id = chat_id
        db.update_workspace(workspace)

        # Set the last_workspace_id in the user
        print(f"Setting last workspace id to {workspace_id}")
        user = db.get_user_by_id(chat.owner)
        user.last_workspace_id = workspace_id
        db.update_user(user)

        # Invalidate connection string
        try:
            db.delete_chat_connection_string(connection_string)
        except Exception as e:
            print(str(e))
            return

        join_room(chat_id)  # Join room

    @socketio.on('chat_message', namespace='/chat')
    def handle_message(message_json: str):
        message_json = json.loads(message_json)
        message = message_json['message']
        chat_id = message_json['chat_id']
        message_string = message_json['message_string']

        print(f"User sent message '{message}' to chat {chat_id}")

        # Load chat
        try:
            chat = db.get_chat_by_id(chat_id)
        except Exception as e:
            print(str(e))
            return

        # Check if message string exists
        try:
            db_message_string = db.get_chat_message_string(message_string)
        except Exception as e:
            print(str(e))
            return

        # Check if message string is expired
        if db_message_string.expires_at < time.time():
            print("Message string expired")
            # Invalidate message string
            try:
                db.delete_chat_message_string(message)
            except Exception as e:
                print(str(e))

        # Check if message string is for the correct chat
        if db_message_string.chat_id != chat_id:
            print("Message string is for the wrong chat")
            return

        # Invalidate message string
        try:
            db.delete_chat_message_string(message)
        except Exception as e:
            print(str(e))
            return

        # Add message to chat history
        chat.add_message(role="user", content=message)
        db.update_chat(chat)

        # Send chat to Chat Queue (STELLA will pick it up from there)
        chat_queue.add_chat(chat_id)

        # Let the user know that the message has been received and queued
        socketio.emit('feedback', json.dumps({"type": "message_received", "message": message, "chat_id": chat_id}),
                      room=chat_id, namespace='/chat')

    @socketio.on('disconnect')
    def disconnect_from_chat():
        chat_id = request.args.get('chat_id')
        print(f"User disconnected from chat {chat_id}")
        leave_room(chat_id)

    return chat_views
