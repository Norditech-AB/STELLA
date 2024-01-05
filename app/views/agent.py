import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import dotenv
import requests
import zipfile
import io
from flask import current_app

'''
To use local webhooks, you need to install the Stripe CLI:
stripe listen --forward-to localhost:5001/webhook
'''

dotenv.load_dotenv()

webhook_secret = os.environ.get("WEBHOOK_SECRET")

agent_views = Blueprint('agent_views', __name__)


@agent_views.route('/agent/download', methods=['GET'])
@jwt_required()
def download_package():
    package_name = request.args.get('query')
    version = request.args.get('version')

    if not package_name:
        return jsonify({"error": "Missing param 'query' "}), 400

    url = "https://download-package-d6iaqsbjgq-uc.a.run.app"
    # Parameters for the API request
    params = {
        "query": package_name,  # Example query
        "version": version      # Set to None or omit if you want the latest version
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Save the downloaded file
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = "package.zip"  # Fallback filename if header is not set
        
        downloaded_version = filename.removesuffix(".zip")

        z = zipfile.ZipFile(io.BytesIO(response.content))
        for file in z.namelist():
            if "__MACOSX/" in file:
                continue
            z.extract(file, path="agents")

        return f"Successfully installed {package_name}:{downloaded_version}", response.status_code
    elif response.status_code == 404:
        return f"Package not found: {package_name}:{version}", response.status_code
    else:
        return f"Failed to download package: {package_name}:{version}, {response.text}", response.status_code
    

@agent_views.route('/agent/reload', methods=['get'])
@jwt_required()
def reload_agents():
    """
    Reloads the agents available in agent storage.
    :return:
    """
    agent_storage = current_app.extensions['agent_storage']

    # Reload the agents
    try:
        agent_storage.reload()
    except Exception as e:
        return jsonify({"msg": f"Critical error occurred when reloading agents. Please restart the server. ({str(e)})"}), 500

    return jsonify({"msg": "Agents reloaded"}), 200
