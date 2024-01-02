import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.db import db
#from app.db.db_handler import DbHandler
import bcrypt
import dotenv


dotenv.load_dotenv()

auth_views = Blueprint('auth_views', __name__)
BCRYPT_SALT = os.getenv('BCRYPT_SALT')


@auth_views.route('/register', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Check if user exists
    user_exists = False
    try:
        existing_user = db.get_user_by_email(email)
        if existing_user:
            user_exists = True
    except Exception as e:  # May throw an exception if the user is not found. Then we still create it.
        pass

    if user_exists:
        return jsonify({"msg": "User already exists"}), 400

    pwd = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8'))
    user = db.create_user(email, pwd)

    return jsonify({"msg": "User created successfully", "email": user.email}), 200


@auth_views.route('/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Check if user exists
    try:
        user = db.get_user_by_email(email)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if password is correct
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Incorrect password."}), 401

