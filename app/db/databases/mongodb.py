import os
from abc import ABC

from bson import ObjectId

import dotenv

from app.db.database_interface import DatabaseInterface
import pymongo

from app.models.user import User
from app.models.workspace import Workspace
from app.models.chat import Chat, ChatConnectionString

dotenv.load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')


class MongoDB(DatabaseInterface, ABC):

    def __init__(self):
        self.instance = pymongo.MongoClient(MONGO_URI)
        self.db = self.instance[MONGO_DB_NAME]

    def create_user(self, email, password) -> User:
        """
        Creates a new user in the database.
        :param email: The email of the user
        :param password: The password of the user
        :return: The created user
        """
        user_id = str(self.db.users.insert_one({
            "email": email,
            "password": password,
            "workspaces": []
        }).inserted_id)

        return User(
            user_id=user_id,
            email=email,
            password=password,
            workspaces=[]
        )

    def create_workspace(self, user_id, name, agents) -> Workspace:
        """
        Creates a new workspace in the database.
        :param user_id: The id of the user that owns the workspace
        :param name: The name of the workspace
        :param agents: The agents in the workspace
        :return: The created workspace
        """
        workspace_id = str(self.db.workspaces.insert_one({
            "owner": user_id,
            "name": name,
            "agents": agents,
            "last_chat_id": None
        }).inserted_id)

        # Add the workspace to the user
        self.db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"workspaces": ObjectId(workspace_id)}})

        return Workspace(
            workspace_id=workspace_id,
            name=name,
            agents=agents,
            owner=user_id,
            last_chat_id=None
        )

    def get_user_workspaces(self, user_id) -> list[str]:
        """
        Gets all the workspaces for the user.
        :param user_id: The id of the user
        :return: The workspaces
        """
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise Exception("User not found")

        workspaces = []
        for workspace_id in user['workspaces']:
            workspaces.append(str(workspace_id))

        return workspaces

    def get_workspace(self, workspace_id) -> Workspace:
        """
        Gets the workspace with the given workspace_id.
        :param workspace_id: The id of the workspace.
        :return: The workspace
        """
        workspace = self.db.workspaces.find_one({"_id": ObjectId(workspace_id)})

        if workspace is None:
            raise Exception("Workspace not found")

        return Workspace(
            workspace_id=str(workspace['_id']),
            name=workspace['name'],
            agents=workspace.get('agents', {}),
            owner=workspace['owner'],
            last_chat_id=workspace.get('last_chat_id', None)
        )

    def delete_workspace(self, workspace_id) -> None:
        """
        Deletes the workspace with the given workspace_id.
        :param workspace_id:
        :return:
        """
        self.db.workspaces.delete_one({"_id": ObjectId(workspace_id)})

    def get_workspace_chats(self, workspace_id) -> list[str]:
        """
        Gets all the chats in the workspace.
        :param workspace_id: The id of the workspace.
        :return: The chats
        """
        chats = []
        for chat in self.db.chats.find({"workspace_id": workspace_id}):
            chats.append(str(chat['_id']))

        return chats

    def get_user_by_id(self, user_id) -> User:
        """
        Finds a user by id.
        :param user_id: The id of the user.
        :return: The user.
        """
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise Exception("User not found")

        return User(
            user_id=str(user['_id']),
            email=user['email'],
            password=user['password'],
            workspaces=user.get('workspaces', [])
        )

    def get_user_by_email(self, email) -> User:
        """
        Finds a user by email.
        :param email: The email of the user.
        :return: The user.
        """
        user = self.db.users.find_one({"email": email})
        if user is None:
            raise Exception("User not found")

        return User(
            user_id=str(user['_id']),
            email=user['email'],
            password=user['password'],
            workspaces=user.get('workspaces', [])
        )

    def update_chat(self, chat: Chat) -> Chat:
        """
        Updates the chat in the database.
        :param chat: The chat to update.
        :return: The updated chat.
        """
        self.db.chats.update_one({"_id": ObjectId(chat.chat_id)}, {"$set": chat.to_dict()})
        return chat

    def get_chat_by_id(self, chat_id) -> Chat:
        """
        Gets the chat with the given chat_id.
        :param chat_id: The id of the chat.
        :return: The chat.
        """
        chat = self.db.chats.find_one({"_id": ObjectId(chat_id)})

        if chat is None:
            raise Exception("Chat not found")

        return Chat(
            chat_id=chat_id,
            workspace_id=chat['workspace_id'],
            owner=chat['owner'],
            chat_history=chat.get('chat_history', []),
            busy=chat.get('busy', False)
        )

    def get_task_data(self, task_id) -> dict:
        """
        Gets the task with the given task_id.
        :param task_id: The id of the task.
        :return: The task.
        """
        task = self.db.tasks.find_one({"_id": ObjectId(task_id)})

        print(f"Getting task {task_id}")
        if task is None:
            raise Exception("Task not found")

        task_data = {
            "chat_id": task['chat_id'],
            "agents": task['agents'],
            "owner": task['owner'],
            "coordinator_agent": task['coordinator_agent'],
            "current_agent": task['current_agent'],
            "memories": task['memories'],
            "parent_task_id": task.get('parent_task_id', None),
            "top_level_task_id": task.get('top_level_task_id', None),
            "completed": task['completed'],
            "task_id": task_id,
            "created_at": task['created_at'],
            "depths": task.get('depths', None),
            "is_top_level": task.get('is_top_level', False),
            "top_level_task_max_depth": task.get('top_level_task_max_depth', None),
            "top_level_task_depth": task.get('top_level_task_depth', None)
        }

        return task_data

    def create_task(self, chat_id, agents, owner, coordinator_agent, current_agent, memories,
                    parent_task_id=None, top_level_task_id=None, completed=False, created_at=None, depths=None,
                    is_top_level=False, top_level_task_max_depth=None, top_level_task_depth=None):
        """
        Creates a new task in the database.
        :param chat_id: The id of the original chat where the message was sent by the user to Stella
        :param agents: All the agents available in the Task.
        :param owner: The user's id
        :param coordinator_agent: The agent that the task was *originally* assigned to
        :param current_agent: The agent that the task is *currently* assigned to
        :param memories: The memories that the task has accumulated (note, parent tasks can also have memories)
        :param parent_task_id: The id of the parent task (if this is a subtask)
        :param top_level_task_id: The id of the top level task
        :param completed: Whether the task is completed or not
        :param created_at: The time the task was created in format "%Y-%m-%d %H:%M:%S" (YYYY-MM-DD HH:MM:SS)
        :param depths: Subtask depths
        :param is_top_level: Whether the task is a top level task or not
        :param top_level_task_max_depth: Max depth of the top level task
        :param top_level_task_depth: Current depth of the top level task
        :return: The created task
        """

        task_data = {
            "chat_id": chat_id,
            "agents": agents,
            "owner": owner,
            "coordinator_agent": coordinator_agent,
            "current_agent": current_agent,
            "memories": memories,
            "parent_task_id": parent_task_id,
            "top_level_task_id": top_level_task_id,
            "completed": completed,
            "created_at": created_at,
            "depths": depths,
            "is_top_level": is_top_level,
            "top_level_task_max_depth": top_level_task_max_depth,
            "top_level_task_depth": top_level_task_depth
        }
        task_id = str(self.db.tasks.insert_one(task_data).inserted_id)
        task_data['task_id'] = str(task_id)

        return task_data

    def create_chat_connection_string(self, chat_id, string, created_at, expires_at, created_by) -> ChatConnectionString:
        """
        Creates a new chat connection string in the database.
        :param chat_id: The id of the chat
        :param string: The connection string
        :param created_at: The time the connection string was created
        :param expires_at: The time the connection string expires
        :param created_by: The user that created the connection string
        :return: The created connection string
        """
        self.db.chat_connection_strings.insert_one({
            "chat_id": chat_id,
            "string": string,
            "created_at": created_at,
            "expires_at": expires_at,
            "created_by": created_by
        })

        return ChatConnectionString(
            chat_id=chat_id,
            string=string,
            created_at=created_at,
            expires_at=expires_at,
            created_by=created_by
        )

    def get_chat_connection_string(self, string) -> ChatConnectionString:
        """
        Gets the chat connection string with the given string.
        :param string: The string of the connection string.
        :return: The connection string.
        """
        connection_string = self.db.chat_connection_strings.find_one({"string": string})

        if connection_string is None:
            raise Exception("Connection string not found")

        return ChatConnectionString(
            chat_id=connection_string['chat_id'],
            string=connection_string['string'],
            created_at=connection_string['created_at'],
            expires_at=connection_string['expires_at'],
            created_by=connection_string['created_by']
        )

    def delete_chat_connection_string(self, string) -> None:
        """
        Deletes the chat connection string with the given string.
        :param string: The string of the connection string.
        :return: None
        """
        self.db.chat_connection_strings.delete_one({"string": string})

    def create_chat_message_string(self, chat_id, string, created_at, expires_at, created_by) -> ChatConnectionString:
        """
        Creates a new chat message string in the database.
        :param chat_id: The id of the chat
        :param string: The connection string
        :param created_at: The time the connection string was created
        :param expires_at: The time the connection string expires
        :param created_by: The user that created the connection string
        :return: The created connection string
        """
        self.db.chat_message_strings.insert_one(
            {
                "chat_id": chat_id,
                "string": string,
                "created_at": created_at,
                "expires_at": expires_at,
                "created_by": created_by
            }
        )

        return ChatConnectionString(
            chat_id=chat_id,
            string=string,
            created_at=created_at,
            expires_at=expires_at,
            created_by=created_by
        )

    def get_chat_message_string(self, string) -> ChatConnectionString:
        """
        Gets the chat message string with the given string.
        :param string: The string of the message string.
        :return: The message string.
        """
        message_string = self.db.chat_message_strings.find_one({"string": string})

        if message_string is None:
            raise Exception("Message string not found")

        return ChatConnectionString(
            chat_id=message_string['chat_id'],
            string=message_string['string'],
            created_at=message_string['created_at'],
            expires_at=message_string['expires_at'],
            created_by=message_string['created_by']
        )

    def delete_chat_message_string(self, string) -> None:
        """
        Deletes the chat message string with the given string.
        :param string: The string of the message string.
        :return: None
        """
        self.db.chat_message_strings.delete_one({"string": string})

    def create_chat(self, workspace_id, user_id) -> Chat:
        """
        Creates a new chat in the database.
        :param workspace_id: The id of the workspace.
        :param user_id: The id of the user.
        :return: The created chat.
        """
        chat_id = str(self.db.chats.insert_one({
            "owner": user_id,
            "workspace_id": workspace_id,
            "chat_history": [],
        }).inserted_id)

        return Chat(
            chat_id=chat_id,
            workspace_id=workspace_id,
            owner=user_id,
            chat_history=[],
        )

    def delete_chat(self, chat_id) -> None:
        """
        Deletes the chat with the given chat_id.
        :param chat_id: The id of the chat.
        :return: None
        """
        self.db.chats.delete_one({"_id": ObjectId(chat_id)})

    def delete_task(self, task_id) -> None:
        """
        Deletes the task with the given task_id.
        :param task_id: The id of the task.
        :return: None
        """
        self.db.tasks.delete_one({"_id": ObjectId(task_id)})

    def delete_user(self, user_id) -> None:
        """
        Deletes the user with the given user_id.
        :param user_id: The id of the user.
        :return: None
        """
        self.db.users.delete_one({"_id": ObjectId(user_id)})


    def get_user_chats(self, user_id) -> list[str]:
        """
        Gets all the chats for the user.
        :param user_id: The id of the user
        :return: The chats
        """
        chats = []
        for chat in self.db.chats.find({"owner": user_id}):
            chats.append(str(chat['_id']))

        return chats

    def update_task_data(self, task_data) -> dict:
        """
        Updates the task in the database.
        :param task_data: The task to update.
        :return: The updated task.
        """
        self.db.tasks.update_one({"_id": ObjectId(task_data['task_id'])}, {"$set": task_data})
        return task_data

    def update_user(self, user: User) -> User:
        """
        Updates the user in the database.
        :param user: The user to update.
        :return: The updated user.
        """
        self.db.users.update_one({"_id": ObjectId(user.id)}, {"$set": user.to_dict()})
        return user

    def update_workspace(self, workspace: Workspace) -> Workspace:
        """
        Updates the workspace in the database.
        :param workspace: The workspace to update.
        :return: The updated workspace.
        """
        self.db.workspaces.update_one({"_id": ObjectId(workspace.id)}, {"$set": workspace.to_dict()})
        return workspace
