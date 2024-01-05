import os
import sqlite3
import json
from abc import ABC

from app.db.database_interface import DatabaseInterface
from app.models.user import User
from app.models.workspace import Workspace
from app.models.chat import Chat, ChatConnectionString

# Load environment variables
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH')  # sqlite.db
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class SQLite(DatabaseInterface, ABC):

    def __init__(self):
        self.conn = sqlite3.connect(os.path.abspath(os.path.join(THIS_FOLDER, '../../', SQLITE_DB_PATH)))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        sql_user = '''
            CREATE TABLE IF NOT EXISTS "user" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "username" TEXT,
                "password" TEXT,
                "workspaces" TEXT,
                "last_workspace_id" INTEGER
            )
        '''

        sql_workspace = '''
            CREATE TABLE IF NOT EXISTS "workspace" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "owner" INTEGER,
                "name" TEXT,
                "agents" TEXT,
                "last_chat_id" INTEGER,
                FOREIGN KEY(owner) REFERENCES user(id)
            )
        '''

        sql_chat = '''
            CREATE TABLE IF NOT EXISTS "chat" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "workspace_id" INTEGER,
                "owner" INTEGER,
                "chat_history" TEXT,
                "busy" INTEGER DEFAULT 0,
                FOREIGN KEY(workspace_id) REFERENCES workspace(id),
                FOREIGN KEY(owner) REFERENCES user(id)
            )
        '''

        sql_task = '''
            CREATE TABLE IF NOT EXISTS "task" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "chat_id" INTEGER,
                "agents" TEXT,
                "owner" INTEGER,
                "coordinator_agent" TEXT,
                "current_agent" TEXT,
                "memories" TEXT,
                "parent_task_id" INTEGER,
                "top_level_task_id" INTEGER,
                "completed" INTEGER DEFAULT 0,
                "created_at" TEXT,
                "depths" TEXT,
                "is_top_level" INTEGER DEFAULT 0,
                "top_level_task_max_depth" INTEGER,
                "top_level_task_depth" INTEGER
            )
        '''

        sql_connection_string = '''
            CREATE TABLE IF NOT EXISTS "chat_connection_string" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "chat_id" INTEGER,
                "string" TEXT,
                "created_at" REAL,
                "expires_at" REAL,
                "created_by" TEXT,
                FOREIGN KEY(chat_id) REFERENCES chat(id),
                FOREIGN KEY(created_by) REFERENCES user(id)
            )
        '''

        cursor.execute(sql_user)
        cursor.execute(sql_workspace)
        cursor.execute(sql_chat)
        cursor.execute(sql_task)
        cursor.execute(sql_connection_string)

        self.conn.commit()

    def _serialize_list(self, data):
        return json.dumps(data)

    def _deserialize_list(self, data):
        return json.loads(data) if data else []

    def create_user(self, username, password) -> User:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO user (username, password, workspaces, last_workspace_id) VALUES (?, ?, ?, ?)",
                       (username, password, json.dumps([]), None))
        user_id = cursor.lastrowid
        self.conn.commit()
        return User(user_id=str(user_id), username=username, password=password, workspaces=[], last_workspace_id=None)

    def create_workspace(self, user_id, name, agents) -> Workspace:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO workspace (owner, name, agents, last_chat_id) VALUES (?, ?, ?, ?)",
                       (user_id, name, json.dumps(agents), None))
        workspace_id = cursor.lastrowid
        self.conn.commit()
        cursor.execute("SELECT workspaces FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        workspaces_list = self._deserialize_list(row['workspaces'])
        workspaces_list.append(workspace_id)
        cursor.execute("UPDATE user SET workspaces = ? WHERE id = ?", (json.dumps(workspaces_list), user_id))
        self.conn.commit()
        return Workspace(workspace_id=str(workspace_id), name=name, agents=agents, owner=user_id, last_chat_id=None)

    def get_user_workspaces(self, user_id) -> list[Workspace]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT workspaces FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("User not found")
        workspaces = self._deserialize_list(row['workspaces'])
        return [self.get_workspace(workspace_id) for workspace_id in workspaces]

    def get_workspace(self, workspace_id) -> Workspace:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM workspace WHERE id = ?", (workspace_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Workspace not found")
        return Workspace(
            workspace_id=str(row['id']),
            name=row['name'],
            agents=self._deserialize_list(row['agents']),
            owner=str(row['owner']),
            last_chat_id=str(row['last_chat_id']) if row['last_chat_id'] else None
        )

    def delete_workspace(self, workspace_id) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM workspace WHERE id = ?", (workspace_id,))
        self.conn.commit()

    def get_workspace_chats(self, workspace_id) -> list[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM chat WHERE workspace_id = ?", (workspace_id,))
        chats = cursor.fetchall()
        return [str(chat['id']) for chat in chats]

    def get_user_by_id(self, user_id) -> User:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("User not found")
        return User(
            user_id=str(row['id']),
            username=row['username'],
            password=row['password'],
            workspaces=self._deserialize_list(row['workspaces']),
            last_workspace_id=str(row['last_workspace_id']) if row['last_workspace_id'] else None
        )

    def get_user_by_username(self, username) -> User:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("User not found")
        return User(
            user_id=str(row['id']),
            username=row['username'],
            password=row['password'],
            workspaces=self._deserialize_list(row['workspaces']),
            last_workspace_id=str(row['last_workspace_id']) if row['last_workspace_id'] else None
        )

    def update_chat(self, chat: Chat) -> Chat:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE chat SET workspace_id = ?, owner = ?, chat_history = ?, busy = ? WHERE id = ?", (
            chat.workspace_id, chat.owner, json.dumps(chat.chat_history), int(chat.busy), chat.chat_id
        ))
        self.conn.commit()
        return chat

    def get_chat_by_id(self, chat_id) -> Chat:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chat WHERE id = ?", (chat_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Chat not found")
        return Chat(
            chat_id=str(chat_id),
            workspace_id=str(row['workspace_id']),
            owner=str(row['owner']),
            chat_history=self._deserialize_list(row['chat_history']),
            busy=bool(row['busy'])
        )

    def get_task_data(self, task_id) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM task WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Task not found")
        task_data = {
            "chat_id": str(row['chat_id']),
            "agents": self._deserialize_list(row['agents']),
            "owner": str(row['owner']),
            "coordinator_agent": row['coordinator_agent'],
            "current_agent": row['current_agent'],
            "memories": self._deserialize_list(row['memories']),
            "parent_task_id": str(row['parent_task_id']) if row['parent_task_id'] else None,
            "top_level_task_id": str(row['top_level_task_id']) if row['top_level_task_id'] else None,
            "completed": bool(row['completed']),
            "task_id": str(task_id),
            "created_at": row['created_at'],
            "depths": self._deserialize_list(row['depths']),
            "is_top_level": bool(row['is_top_level']),
            "top_level_task_max_depth": row['top_level_task_max_depth'],
            "top_level_task_depth": row['top_level_task_depth']
        }
        return task_data

    def create_task(self, chat_id, agents, owner, coordinator_agent, current_agent, memories,
                    parent_task_id=None, top_level_task_id=None, completed=False, created_at=None, depths=None,
                    is_top_level=False, top_level_task_max_depth=None, top_level_task_depth=None):
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO task (chat_id, agents, owner, coordinator_agent, current_agent, memories, parent_task_id, top_level_task_id, completed, created_at, depths, is_top_level, top_level_task_max_depth, top_level_task_depth) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chat_id, json.dumps(agents), owner, coordinator_agent, current_agent, json.dumps(memories), parent_task_id,
             top_level_task_id, int(completed), created_at, json.dumps(depths), int(is_top_level),
             top_level_task_max_depth,
             top_level_task_depth)
        )

        task_id = cursor.lastrowid
        self.conn.commit()
        task_data = {
            "task_id": str(task_id),
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

        print(f"CREATING TASK:")
        print(json.dumps(task_data, indent=4))

        return task_data

    def create_chat_connection_string(self, chat_id, string, created_at, expires_at,
                                      created_by) -> ChatConnectionString:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO chat_connection_string (chat_id, string, created_at, expires_at, created_by) VALUES (?, ?, ?, ?, ?)",
            (chat_id, string, created_at, expires_at, created_by))
        self.conn.commit()
        return ChatConnectionString(
            chat_id=chat_id,
            string=string,
            created_at=created_at,
            expires_at=expires_at,
            created_by=created_by
        )

    def get_chat_connection_string(self, string) -> ChatConnectionString:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chat_connection_string WHERE string = ?", (string,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Connection string not found")
        return ChatConnectionString(
            chat_id=str(row['chat_id']),
            string=row['string'],
            created_at=row['created_at'],
            expires_at=row['expires_at'],
            created_by=str(row['created_by'])
        )

    def delete_chat_connection_string(self, string) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chat_connection_string WHERE string = ?", (string,))
        self.conn.commit()

    def create_chat(self, workspace_id, user_id) -> Chat:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO chat (workspace_id, owner, chat_history, busy) VALUES (?, ?, ?, ?)",
                       (workspace_id, user_id, json.dumps([]), 0))
        chat_id = cursor.lastrowid
        self.conn.commit()
        return Chat(chat_id=str(chat_id), workspace_id=workspace_id, owner=user_id, chat_history=[], busy=False)

    def delete_chat(self, chat_id) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chat WHERE id = ?", (chat_id,))
        self.conn.commit()

    def delete_task(self, task_id) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
        self.conn.commit()

    def delete_user(self, user_id) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        self.conn.commit()

    def get_user_chats(self, user_id) -> list[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM chat WHERE owner = ?", (user_id,))
        chats = cursor.fetchall()
        return [str(chat['id']) for chat in chats]

    def update_task_data(self, task_data) -> dict:
        cursor = self.conn.cursor()
        print(f"UPDATING TASK")
        print(json.dumps(task_data))
        cursor.execute(
            "UPDATE task SET chat_id = ?, agents = ?, owner = ?, coordinator_agent = ?, current_agent = ?, memories = ?, parent_task_id = ?, top_level_task_id = ?, completed = ?, created_at = ?, depths = ?, is_top_level = ?, top_level_task_max_depth = ?, top_level_task_depth = ? WHERE id = ?",
            (
                task_data['chat_id'],
                json.dumps(task_data['agents']),
                task_data['owner'],
                task_data['coordinator_agent'],
                task_data['current_agent'],
                json.dumps(task_data['memories']),
                task_data.get('parent_task_id', None),
                task_data.get('top_level_task_id', None),
                int(task_data.get('completed', False)),
                task_data.get('created_at', None),
                json.dumps(task_data.get('depths', None)),
                int(task_data.get('is_top_level', False)),
                task_data.get('top_level_task_max_depth', None),
                task_data.get('top_level_task_depth', None),
                task_data.get('task_id', None)
            ))
        self.conn.commit()
        return task_data

    def update_user(self, user: User) -> User:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE user SET username = ?, password = ?, workspaces = ?, last_workspace_id = ? WHERE id = ?", (
            user.username,
            user.password,
            json.dumps(user.workspaces),
            user.last_workspace_id,
            user.id
        ))
        self.conn.commit()
        return user

    def update_workspace(self, workspace: Workspace) -> Workspace:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE workspace SET name = ?, agents = ?, owner = ?, last_chat_id = ? WHERE id = ?", (
            workspace.name,
            json.dumps(workspace.agents),
            workspace.owner,
            workspace.last_chat_id,
            workspace.id
        ))
        self.conn.commit()
        return workspace

    def create_chat_message_string(self, chat_id, string, created_at, expires_at, created_by) -> ChatConnectionString:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO chat_connection_string (chat_id, string, created_at, expires_at, created_by) VALUES (?, ?, ?, ?, ?)", (chat_id, string, created_at, expires_at, created_by))
        self.conn.commit()
        return ChatConnectionString(
            chat_id=chat_id,
            string=string,
            created_at=created_at,
            expires_at=expires_at,
            created_by=created_by
        )

    def get_chat_message_string(self, string) -> ChatConnectionString:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chat_connection_string WHERE string = ?", (string,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("Message string not found")
        return ChatConnectionString(
            chat_id=str(row['chat_id']),
            string=row['string'],
            created_at=row['created_at'],
            expires_at=row['expires_at'],
            created_by=str(row['created_by'])
        )

    def delete_chat_message_string(self, string) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chat_connection_string WHERE string = ?", (string,))
        self.conn.commit()