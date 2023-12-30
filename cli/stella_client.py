import requests
from cli_design import *
from tabulate import tabulate
import socketio
import json
import time
import requests
import zipfile
import io

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
ENDC = '\033[0m'  # Reset to default color

VISS_GREEN = '\033[38;5;43m'

CONFIG = {
    "base_url": "http://localhost:5001/",
    "socket_url": "http://localhost:5001/chat/connect",
    "email": "demo@spotify.se",  # TODO: Add email
    "password": "123",  # TODO: Add password
}

SOCKETIO_NAMESPACE = "/chat"


def compose_url(endpoint):
    return f"{CONFIG['base_url']}{endpoint}"


class StellaClient:
    def __init__(self):
        self.spinner = Spinner()

        self.base_url = "http://localhost:5001/"

        # test connection

        self.workspace_id = None
        self.chat_id = None
        self.connection_string = None

        # existing initialization code...
        data = self.read_local_config()
        self.access_token = data["session_token"]
        self.workspace_id = data["current_workspace"]
        self.chat_id = data["current_chat"]

        # ws_id = self.add_workspace()
        # chat_id = self.create_chat(ws_id)
        # self.connect_to_chat(chat_id)

        # self.login(CONFIG["email"], CONFIG["password"])

        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect, namespace=SOCKETIO_NAMESPACE)
        self.sio.on('message', self.on_message, namespace=SOCKETIO_NAMESPACE)
        self.sio.on('chat_information', self.on_message, namespace=SOCKETIO_NAMESPACE)
        self.sio.on('disconnect', self.on_disconnect, namespace=SOCKETIO_NAMESPACE)

        self.should_wait_for_response = True
        self.waiting_for_response = False
        self.initial_message = None

    def read_local_config(self):
        try:
            # Read the existing data
            with open("data.json", "r") as file:
                data = json.load(file)

            # Check if keys exist and update if necessary
            data_updated = False
            if "session_token" not in data:
                data["session_token"] = ""
                data_updated = True
            if "current_workspace" not in data:
                data["current_workspace"] = ""
                data_updated = True

            # Write the updated data back, if necessary
            if data_updated:
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)

            return data

        except Exception:
            with open("data.json", "w") as file:
                data = {"session_token": "", "current_workspace": ""}
                json.dump(data, file, indent=4)
                return data

    def save_to_config(self, **kwargs):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

            # Update data with the key-value pairs provided in kwargs
            data.update(kwargs)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"Error: {e}")

    # auth user logic
    def compose_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    def is_authenticated(self):
        url = compose_url(f"workspace")
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}

        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            print("could not establish connection to server, try", VISS_GREEN + "stella serve" + ENDC)
            exit(0)

        if response.status_code != 200:
            return False
        return True

    def login(self, email, password):
        try:
            response = requests.post(
                self.compose_url("auth/login"),
                json={"email": email, "password": password}
            )
            if response.status_code != 200:
                print("Login failed")
                return None
            access_token = response.json()["access_token"]
            print("Login successful.")

            # save session
            self.save_to_config(session_token=access_token)

            self.access_token = access_token
            return access_token
        except Exception as e:
            print(f"Login failed: {e}")

    def switch_workspace(self, workspace_id):
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.get(compose_url(f"workspace/{workspace_id}"), headers=headers)
        if response.status_code == 500:
            print("Workspace not found")
        elif response.status_code != 200:
            print("something went wrong")
        else:
            self.workspace_id = workspace_id
            self.connect_to_chat()
            print("current workspace:", workspace_id)
            print("current chat id:", self.chat_id)

    def install_agent(self, package_name, version=None):
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.get(compose_url(f"agent/download"), headers=headers,
                                params={"query": package_name, "version": version})

        if version is None:
            version = "latest"

        if response.status_code == 200:
            print(f"Succesfully installed {package_name}:{version}")
        elif response.status_code == 404:
            print(f"Package not found: {package_name}:{version}")
        else:
            print(f"Failed to download package: {package_name}:{version}, {response.text}")

    def upload_agent(self, package_name="viss_ai/DemoAgents"):
        url = "https://package.viss.ai/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            # Assuming the package is a zip file
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall(path="../app/agents")

    def logout(self):
        if self.access_token:
            self.access_token = None
            try:
                with open("config.json", "r+") as file:
                    data = json.load(file)
                    data["session"] = {}  # Clear session data
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                print("Logout successful.")
            except FileNotFoundError:
                print("Config file not found.")
        else:
            print("Not logged in")

    def register(self, email, password):
        try:
            response = requests.post(
                self.compose_url("register"),
                json={"email": email, "password": password}
            )
            print("Registration successful. Please login.")

        except Exception as e:
            print(f"Registration failed: {e}")

    def get_current_workspace(self):
        return self.workspace_id

    # workspace logic

    def add_workspace(self):
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.post(compose_url("workspace"), headers=headers)
        if response.status_code != 200:
            raise Exception(
                "Request failed with status code: {}, Message: {}".format(response.status_code, response.text))
        print(response.json())
        workspace_id = response.json()["workspace"]["id"]

        print("Workspace id:", workspace_id)
        return workspace_id

    def rename_workspace(self, workspace_id, name):
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.put(compose_url(f"workspace/{workspace_id}/rename"), headers=headers, json={"name": name})
        if response.status_code != 200:
            print("Failed to rename workspace")

        print("workspace name:", name)
        return workspace_id

    def get_all_workspaces(self):
        url = compose_url(f"workspace")
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Workspace not found")
            exit(0)
        else:
            workspaces = response.json()["workspaces"]
            return workspaces

    def get_workspace_by_id(self, workspace_id=None):
        url = compose_url(f"workspace/{workspace_id}")
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Workspace not found")
        else:
            workspace = response.json()["workspace"]
            return workspace

        return None

    def delete_workspace(self, workspace_id):
        print("Delete workspace", workspace_id)

    def add_agent(self, agent_id):
        url = compose_url(f"workspace/{self.workspace_id}/agent")
        data = {"agent_id": agent_id}

        response = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.access_token}"})
        if response.status_code != 200:
            print("Failed to add agent")
        else:
            print("Agent added")

    def create_chat(self, workspace_id):
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        response_chat = requests.post(compose_url(f"chat?workspace_id={workspace_id}"), headers=headers)
        print(response_chat.json())
        chat_id = response_chat.json()["chat"]["chat_id"]
        print(f"New Chat ID: {chat_id}")
        if chat_id is None:
            raise Exception("Chat ID was not returned.")
        print(f"New Chat ID: {chat_id}")
        return chat_id

    # chat logic
    def on_connect(self):
        print("=== Connection opened ===")

    @staticmethod
    def on_disconnect():
        print("=== Connection closed ===")

    def on_message(self, message):
        self.spinner.stop()
        print_with_delay(message)
        self.waiting_for_response = False

    def get_connection_string(self, chat_id, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(compose_url(f"chat/authorize?chat_id={chat_id}"), headers=headers)
        if response.status_code != 200:
            raise Exception(
                "Request failed with status code: {}, Message: {}".format(response.status_code, response.text))
        print(response.json())
        return response.json()["string"]

    def disconnect_from_chat(self):
        self.sio.disconnect()
        print("Disconnected from chat.")

    def connect_to_chat(self):

        # check if workspace exist
        ws_data = self.get_workspace_by_id(self.workspace_id)
        if ws_data is None:
            self.workspace_id = self.add_workspace()
            self.chat_id = self.create_chat(self.workspace_id)
        else:
            if self.chat_id != ws_data['last_chat_id']:
                self.chat_id = ws_data['last_chat_id']

            if self.chat_id is None:
                self.chat_id = self.create_chat(self.workspace_id)

        # TODO check if chat exist

        self.save_to_config(current_workspace=self.workspace_id, current_chat=self.chat_id)

        print(f"Connecting to chat {self.chat_id}...")

        if self.connection_string is not None:
            print(f"Closing current connection...")
            self.disconnect_from_chat()
            self.connection_string = None

        # Connect to chat
        if self.connection_string is None:
            print(f"Getting connection string...")
            self.connection_string = self.get_connection_string(self.chat_id, self.access_token)
            print(f"Connection string: {self.connection_string}")
            self.sio.connect(
                f"{CONFIG['socket_url']}?chat_id={self.chat_id}&connection_string={self.connection_string}",
                namespaces=[SOCKETIO_NAMESPACE])

    def send_message(self, message: str, chat_id=None):
        if self.waiting_for_response:
            return

        if chat_id is None:
            chat_id = self.chat_id

        self.spinner.start()

        # Get a message secret
        response = requests.get(
            compose_url(f"chat/authorize/message?chat_id={chat_id}"),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        message_string = response.json()["string"]

        json_data = {
            "message": message,
            "chat_id": chat_id,
            "message_string": message_string,
        }

        self.sio.emit("chat_message", json.dumps(json_data), namespace=SOCKETIO_NAMESPACE)
        self.waiting_for_response = True


def print_with_delay(text):
    words = text.split()
    for word in words:
        colored_word = VISS_GREEN + word + ENDC
        print(colored_word, end=" ", flush=True)
        time.sleep(0.04)
    print("\n")  # Move to the next line after the sentence is completed


if __name__ == '__main__':
    cli_wrapper = StellaClient()
    # cli_wrapper.login('demo@spotify.se', '123')
    # input("")
    # cli_wrapper.logout()
    # cli_wrapper.start_server()
    workspace_id = cli_wrapper.create_workspace()
    chat_id = cli_wrapper.create_chat(workspace_id)
    cli_wrapper.connect_to_chat(chat_id)

    while True:
        message = "Hi"
        cli_wrapper.send_message(message)
        cli_wrapper.send_message(message)
    # response = cli_wrapper.send_message("Hello")
    # cli_wrapper.status()
