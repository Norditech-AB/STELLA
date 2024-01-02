from flask import Blueprint, jsonify

utils_views = Blueprint('utils_views', __name__)


@utils_views.route('/ping', methods=['GET'])
def pong():
    return jsonify({"msg": "pong"}), 200


