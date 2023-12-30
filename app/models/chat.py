
class Chat:
    """
    Stores information about a chat
    """
    def __init__(self, chat_id, workspace_id, owner, chat_history=None, busy=None):
        self.chat_id = chat_id
        self.workspace_id = workspace_id
        self.owner = owner
        self.chat_history = chat_history if chat_history is not None else []
        self.busy = busy if busy is not None else False

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "workspace_id": self.workspace_id,
            "owner": self.owner,
            "chat_history": self.chat_history,
            "busy": self.busy
        }

    def add_message(self, role, content):
        self.chat_history.append({"role": role, "content": content})

    def get_chat_history(self, length=None):
        if length is not None:
            # Get <length> latest messages
            return self.chat_history[-length:]
        return self.chat_history

    def clear_chat_history(self):
        self.chat_history = []

    def __str__(self):
        return f"Chat(chat_id={self.chat_id}, workspace_id={self.workspace_id}, owner={self.owner}, " \
                  f"chat_history={self.chat_history}, busy={self.busy})"


class ChatConnectionString:
    def __init__(self, chat_id, string, created_at, expires_at, created_by):
        self.chat_id = chat_id
        self.string = string
        self.created_at = created_at
        self.expires_at = expires_at
        self.created_by = created_by

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "string": self.string,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "created_by": self.created_by
        }


class ChatMessageString:
    def __init__(self, chat_id, string, created_at, expires_at, created_by):
        self.chat_id = chat_id
        self.string = string
        self.created_at = created_at
        self.expires_at = expires_at
        self.created_by = created_by

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "string": self.string,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "created_by": self.created_by
        }

