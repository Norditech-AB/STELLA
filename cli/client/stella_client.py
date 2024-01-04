import os

from .cli_design import *
import socketio
import json
import time
import requests
import zipfile
import io


class Session:
    def __init__(self, session_file_path=None):
        self.session_file_path = session_file_path
        self.access_token = None
        self.workspace_id = None
        self.chat_id = None
        self.chat_connection_string = None
        self.chat_message_string = None

        self.load_session()

    def load_session(self):
        # If a session file is not provided, create it in the current directory
        if self.session_file_path is None:
            self.session_file_path = os.path.join(os.path.dirname(__file__), "../session.json")

        # If the session file does not exist, create it
        if not os.path.exists(self.session_file_path):
            with open(self.session_file_path, "w+") as file:
                json.dump({}, file)

        try:
            # Load the session file
            with open(self.session_file_path, "r") as file:
                session_dict = json.load(file)
                self.access_token = session_dict.get("access_token", None)
                self.workspace_id = session_dict.get("workspace_id", None)
                self.chat_id = session_dict.get("chat_id", None)
                self.chat_connection_string = session_dict.get("chat_connection_string", None)
                self.chat_message_string = session_dict.get("chat_message_string", None)
        except Exception as e:
            print_error(f"(Session error: {e})")
            print_info(f"Could not load session file. Generating a new one.")
            return {}

    def save_session(self):
        with open(self.session_file_path, "w+") as file:
            json.dump(self.to_dict(), file, indent=4)

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "workspace_id": self.workspace_id,
            "chat_id": self.chat_id,
            "chat_connection_string": self.chat_connection_string,
            "chat_message_string": self.chat_message_string,
        }


class StellaClient:
    def __init__(self, host=None, port=None, session_file_path=None, ssl=False):
        self.spinner = Spinner()
        self.host = host
        self.port = port
        self.ssl = ssl
        self.socket_url = f"{'https://' if ssl else 'http://'}{self.host}{':' if self.port else ''}{self.port}/chat/connect"
        self.socketio_namespace = "/chat"

        self.session = Session(session_file_path=session_file_path)

        self.sio = socketio.Client()
        self.sio.on('connect', self.on_connect, namespace=self.socketio_namespace)
        self.sio.on('message', self.on_message, namespace=self.socketio_namespace)
        self.sio.on('chat_information', self.on_message, namespace=self.socketio_namespace)
        self.sio.on('disconnect', self.on_disconnect, namespace=self.socketio_namespace)

        self.should_wait_for_response = True
        self.waiting_for_response = False
        self.initial_message = None

    def auth_headers(self):
        # Check if the user is logged in
        if self.session.access_token is None:
            return {}
        headers = {"Authorization": f"Bearer {self.session.access_token}", "Content-Type": "application/json"}
        return headers

    def verify_connection(self):
        """
        Verify that a connection to the server can be established.
        :return:
        """
        try:
            response = requests.get(self.compose_url("ping"))
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    def compose_url(self, endpoint):
        return f"{'https://' if self.ssl else 'http://'}{self.host}{':' if self.port else ''}{self.port}/{endpoint}"

    def login(self, username, password):
        try:
            response = requests.post(
                self.compose_url("auth/login"),
                json={"username": username, "password": password}
            )
            if response.status_code != 200:
                print_error("Login failed, please try again. (Wrong username or password)")
                return None
            access_token = response.json()["access_token"]
            print_success("Login successful.")

            # Save access token to session
            self.session.access_token = access_token
            self.session.save_session()

            return access_token
        except Exception as e:
            print_error(f"Login failed. Please try again. ({e})")

    def connect_to_workspace(self, workspace_id):
        response = requests.get(self.compose_url(f"workspace/{workspace_id}"), headers=self.auth_headers())
        if response.status_code == 500:
            print_error(f"Workspace with ID {workspace_id} not found.")
        elif response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            print_error("Failed to connect to workspace ({}).".format(response.status_code))
        else:
            self.session.workspace_id = workspace_id
            # Create a new chat
            self.create_chat(workspace_id)
            self.session.save_session()
            self.connect_to_chat()
            print_success("Successfully connected to workspace.")

    def install_agent(self, package_name, version=None):
        response = requests.get(self.compose_url(f"agent/download"), headers=self.auth_headers(),
                                params={"query": package_name, "version": version})

        if version is None:
            version = "latest"

        if response.status_code == 200:
            print_success(f"Successfully installed {package_name}:{version}")
        elif response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code == 404:
            print_info(f"Package not found: {package_name}:{version}")
        else:
            print_error(f"Failed to download package: {package_name}:{version}, {response.text}")

    def logout(self):
        if self.session.access_token:
            self.session.access_token = None
            self.session.save_session()
            print_success("Logout successful.")
        else:
            print_info("Currently not logged in.")

    def register(self, username, password):
        try:
            response = requests.post(
                self.compose_url("register"),
                json={"username": username, "password": password}
            )
            if response.status_code != 200:
                print_error("Registration failed, please try again.")
                return None
            print_success("Registration successful.")

        except Exception as e:
            print_error(f"Registration failed. ({e})")

    def create_workspace(self, name=None):
        if name:
            response = requests.post(self.compose_url("workspace"), headers=self.auth_headers(), json={"name": name})
        else:
            response = requests.post(self.compose_url("workspace"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
            return None
        elif response.status_code != 200:
            raise Exception(
                "Request to create a new workspace failed with status code: {}, Message: {}".format(
                    response.status_code, response.text))
        workspace_id = response.json()["workspace"]["id"]
        self.session.workspace_id = workspace_id
        self.session.save_session()
        print_success(f"Workspace {'named ' + name + ' ' if name else ''}created.")
        return workspace_id

    def rename_workspace(self, name):
        response = requests.put(self.compose_url(f"workspace/{self.session.workspace_id}/rename"), headers=self.auth_headers(),
                                json={"name": name})

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
            return None
        elif response.status_code != 200:
            raise Exception(
                "Request to rename workspace failed with status code: {}, Message: {}".format(response.status_code,
                                                                                              response.text))
        print_success(f"Workspace successfully renamed to {name}.")
        return name

    def get_all_workspaces(self):
        response = requests.get(self.compose_url("workspace"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
            return None
        elif response.status_code != 200:
            print_error("Failed to get workspaces. ({}).".format(response.status_code))
            exit(0)
        else:
            workspaces = response.json()["workspaces"]
            return workspaces

    def get_workspace_by_id(self, workspace_id=None):
        response = requests.get(self.compose_url(f"workspace/{workspace_id}"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            raise Exception("Failed to get workspace. ({}).".format(response.status_code))
        else:
            workspace = response.json()["workspace"]
            return workspace

    def delete_workspace(self, workspace_id):
        response = requests.delete(self.compose_url(f"workspace/{workspace_id}"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            print_error("Failed to delete workspace. ({}).".format(response.status_code))
        else:
            print_success("Workspace deleted.")

    def add_agent(self, agent_id):
        response = requests.post(self.compose_url(f"workspace/{self.session.workspace_id}/agent"), headers=self.auth_headers(),
                                 json={"agent_id": agent_id})

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            print_error("Failed to add agent. ({}).".format(response.status_code))
        else:
            print_success(f"Agent ({agent_id}) added to current workspace successfully.")

    def remove_agent(self, agent_id):
        response = requests.delete(self.compose_url(f"workspace/{self.session.workspace_id}/agent"), headers=self.auth_headers(),
                                    json={"agent_id": agent_id})

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            print_error("Failed to remove agent. ({}).".format(response.status_code))
        else:
            print_info(f"Agent ({agent_id}) removed from current workspace successfully.")

    def create_chat(self, workspace_id):
        response = requests.post(self.compose_url(f"chat?workspace_id={workspace_id}"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            raise Exception(
                "Request to create a new chat failed with status code: {}, Message: {}".format(
                    response.status_code, response.text))
        chat_id = response.json()["chat"]["chat_id"]
        if chat_id is None:
            raise Exception("Chat ID is was not returned from the server. Critical error, aborting.")
        self.session.chat_id = chat_id
        return chat_id

    @staticmethod
    def on_connect():
        pass
        # print_success("Successfully connected to chat.")

    @staticmethod
    def on_disconnect():
        pass
        # print_info("Disconnected from chat.")

    def on_message(self, message):
        # Stop the spinner
        self.spinner.stop()
        # If the message is a chat message, print it
        print_with_delay(message)
        self.waiting_for_response = False

    def get_connection_string(self, chat_id):
        response = requests.get(self.compose_url(f"chat/authorize?chat_id={chat_id}"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            raise Exception(
                "Request to get a chat connection authorization string failed with status code: {}, Message: {}".format(
                    response.status_code, response.text))
        connection_string = response.json()["string"]
        return connection_string

    def disconnect_from_chat(self):
        self.sio.disconnect()

    def connect_to_chat(self):
        # Disconnect from chat if already connected
        self.disconnect_from_chat()

        # Connect to chat
        self.session.chat_connection_string = self.get_connection_string(self.session.chat_id)
        self.sio.connect(
            f"{self.socket_url}?chat_id={self.session.chat_id}&connection_string={self.session.chat_connection_string}",
            namespaces=[self.socketio_namespace])

        # Update session
        self.session.save_session()

    def send_message(self, message: str, chat_id=None):
        # Check if we're currently connected to a chat/workspace
        if self.session.chat_id is None or self.session.workspace_id is None:
            print_error("You are not connected to a chat or workspace.")
            return

        # If we're waiting for a response, don't send another message
        if self.waiting_for_response:
            return

        # If the chat id is not provided, use the one from the session
        chat_id = chat_id or self.session.chat_id

        # Start the spinner
        self.spinner.start()

        # Get a message authorization string from the server
        response = requests.get(
            self.compose_url(f"chat/authorize/message?chat_id={chat_id}"),
            headers=self.auth_headers()
        )

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
            self.spinner.stop()
            return
        elif response.status_code != 200:
            self.spinner.stop()
            raise Exception(
                "Request to get a message authorization string failed with status code: {}, Message: {}".format(
                    response.status_code, response.text))
        self.session.chat_message_string = response.json()["string"]

        # Send the message
        json_data = {
            "message": message,
            "chat_id": chat_id,
            "message_string": self.session.chat_message_string,
        }
        self.sio.emit("chat_message", json.dumps(json_data), namespace=self.socketio_namespace)
        self.waiting_for_response = True

    def get_user(self):
        response = requests.get(self.compose_url("user"), headers=self.auth_headers())

        if response.status_code == 401:
            print_error(f"You are not authenticated. Please login.")
        elif response.status_code != 200:
            raise Exception(
                "Request to get a user failed with status code: {}, Message: {}".format(
                    response.status_code, response.text))
        return response.json()["user"]

    def is_logged_in(self):
        """
        Attempts to fetch the current user information from the server.
        If the request fails, the user is not logged in.
        :return:
        """
        try:
            self.get_user()
            return True
        except Exception as e:
            return False

    def connect_latest(self):
        """
        Attempts to connect to the latest chat & workspace, if any.
        Returns True if the connection was successful, False otherwise.
        :return:
        """
        if self.session.access_token:
            # Attempt to fetch the user information from the server
            try:
                user = self.get_user()
            except Exception as e:
                from cli.utils.exceptions import UserNotFoundException
                raise UserNotFoundException("User not found. Please login again.".format(e))

            # If the user has a last workspace id, fetch it and connect.
            if user["last_workspace_id"]:
                try:
                    workspace = self.get_workspace_by_id(user["last_workspace_id"])
                except Exception as e:
                    return False
                self.session.workspace_id = workspace["id"]
                self.session.save_session()
                self.connect_to_workspace(workspace["id"])


def print_with_delay(text):
    words = text.split()
    for word in words:
        colored_word = VISS_GREEN + word + ENDC
        print(colored_word, end=" ", flush=True)
        time.sleep(0.02)
    print("\n")  # Move to the next line after the sentence is completed
