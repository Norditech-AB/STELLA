import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.db import db
import dotenv

dotenv.load_dotenv()

workspace_views = Blueprint('workspace_views', __name__)
BCRYPT_SALT = os.getenv('BCRYPT_SALT')


@workspace_views.route('/workspace', methods=['POST'])
@jwt_required()
def create_workspace():
    """
    Creates a new workspace for the user in the database.
    :return:
    """
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True)

    name = json_data.get('name', "Untitled Workspace") if json_data else "Untitled Workspace"

    # Create the workspace
    workspace = db.create_workspace(
        user_id=user_id,
        name=name,
        agents={}
    )

    return jsonify({"msg": "Workspace created", "workspace": workspace.to_dict()}), 200


@workspace_views.route('/workspace', methods=['GET'])
@jwt_required()
def get_workspaces():
    """
    Gets all the workspaces for the user.
    :return:
    """
    user_id = get_jwt_identity()

    workspaces = db.get_user_workspaces(user_id)

    return jsonify({"workspaces": workspaces}), 200


@workspace_views.route('/workspace/<workspace_id>', methods=['GET'])
@jwt_required()
def get_workspace(workspace_id):
    """
    Gets the workspace with the given workspace_id.
    :param workspace_id:
    :return:
    """
    user_id = get_jwt_identity()

    workspace = db.get_workspace(workspace_id)

    # Check if the user has access to the workspace
    if workspace.owner != user_id:
        return jsonify({"msg": "User does not have access to the workspace"}), 403

    return jsonify({"workspace": workspace.to_dict()}), 200


@workspace_views.route('/workspace/<workspace_id>', methods=['DELETE'])
@jwt_required()
def delete_workspace(workspace_id):
    """
    Deletes the workspace with the given workspace_id.
    :param workspace_id:
    :return:
    """
    user_id = get_jwt_identity()

    # Find the workspace in the database
    try:
        workspace = db.get_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if the user is the owner of the workspace
    if workspace.owner != user_id:
        return jsonify({"msg": "User does not have access to the workspace"}), 403

    # Delete the workspace
    try:
        db.delete_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    return jsonify({"msg": "Workspace deleted"}), 200


@workspace_views.route('/workspace/<workspace_id>/chats', methods=['GET'])
@jwt_required()
def get_workspace_chats(workspace_id):
    """
    Fetch all chats for the given workspace.
    :param workspace_id:
    :return:
    """
    # Find the workspace in the database
    try:
        workspace = db.get_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if the user is the owner of the workspace
    if workspace.owner != get_jwt_identity():
        return jsonify({"msg": "User does not have access to the workspace"}), 403

    # Get all chats for the workspace
    try:
        chats = db.get_workspace_chats(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    return jsonify({"chats": chats}), 200


@workspace_views.route('/workspace/<workspace_id>/agent', methods=['POST'])
@jwt_required()
def add_agent(workspace_id):
    """
    Adds an agent to the workspace.
    :param workspace_id:
    :return:
    """
    # Make sure an agent_id is passed as a parameter
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    agent_id = request.json.get('agent_id', None)
    if agent_id is None:
        return jsonify({"msg": "Missing agent_id parameter"}), 400

    # TODO: Check if agent_id is valid (?)

    user_id = get_jwt_identity()

    # Find the workspace in the database
    try:
        workspace = db.get_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if the user is the owner of the workspace
    if workspace.owner != user_id:
        return jsonify({"msg": "User is not the owner of the workspace"}), 403

    # Add the agent to the workspace agents
    workspace.agents[agent_id] = {}

    # Update the workspace in the database
    try:
        db.update_workspace(workspace)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    return jsonify({"msg": "Agent added to Workspace."}), 200


@workspace_views.route('/workspace/<workspace_id>/agent', methods=['DELETE'])
@jwt_required()
def remove_agent(workspace_id):
    """
    Removes an agent from the workspace.
    :param workspace_id:
    :return:
    """
    # Make sure an agent_id is passed as a parameter
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    agent_id = request.json.get('agent_id', None)
    if agent_id is None:
        return jsonify({"msg": "Missing agent_id parameter"}), 400

    user_id = get_jwt_identity()

    # Find the workspace in the database
    try:
        workspace = db.get_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if the user is the owner of the workspace
    if workspace.owner != user_id:
        return jsonify({"msg": "User is not the owner of the workspace"}), 403

    # Remove the agent from the workspace agents
    workspace.agents.pop(agent_id, None)

    # Update the workspace in the database
    try:
        db.update_workspace(workspace)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    return jsonify({"msg": "Agent removed"}), 200


@workspace_views.route('/workspace/<workspace_id>/rename', methods=['PUT'])
@jwt_required()
def rename_workspace(workspace_id):
    """
    Renames the workspace with the given workspace_id.
    :param workspace_id:
    :return:
    """
    # Make sure a name is passed as a parameter
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    name = request.json.get('name', None)
    if name is None:
        return jsonify({"msg": "Missing name parameter"}), 400

    user_id = get_jwt_identity()

    # Find the workspace in the database
    try:
        workspace = db.get_workspace(workspace_id)
    except Exception as e:
        return jsonify({"msg": str(e)}), 404

    # Check if the user is the owner of the workspace
    if workspace.owner != user_id:
        return jsonify({"msg": "User is not the owner of the workspace"}), 403

    # Rename the workspace
    workspace.name = name

    # Update the workspace in the database
    try:
        db.update_workspace(workspace)
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

    return jsonify({"msg": "Workspace renamed"}), 200
