import os

import bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.db import db
import dotenv

dotenv.load_dotenv()

user_views = Blueprint('user_views', __name__)

BCRYPT_SALT = os.getenv('BCRYPT_SALT')


@user_views.route('/user/username', methods=['PUT'])
@jwt_required()
def change_username():
    """
    Change the username for a user
    :return:
    """
    json_data = request.get_json()
    user_id = get_jwt_identity()

    # Find the user in the database
    try:
        user = db.get_user_by_id(user_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Get the settings from the request (if they exist)
    username = json_data.get('username', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    user.username = username

    db.update_user(user)

    return jsonify({"msg": "Username updated"}), 200


@user_views.route('/user/password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change the password for a user
    :return:
    """
    json_data = request.get_json()
    user_id = get_jwt_identity()

    # Find the user in the database
    try:
        user = db.get_user_by_id(user_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Get the settings from the request (if they exist)
    password = json_data.get('password', None)

    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    pwd = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))

    if password is not None:
        user.password = pwd

    db.update_user(user)

    return jsonify({"msg": "Password updated"}), 200


@user_views.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """
    Get the settings for a user
    :return:
    """
    user_id = get_jwt_identity()

    # Find the user in the database
    user = db.get_user_by_id(user_id)

    return jsonify({"user": user.to_dict()}), 200



