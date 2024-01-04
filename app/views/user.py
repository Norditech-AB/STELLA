from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.db import db
import dotenv

dotenv.load_dotenv()

user_views = Blueprint('user_views', __name__)


@user_views.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    """
    Update the settings for a user
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
    if username is not None:
        user.username = username

    return jsonify({"msg": "User updated"}), 200


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



