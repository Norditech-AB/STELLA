class User:
    def __init__(self, user_id, username, password, workspaces=None, last_workspace_id=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.workspaces = workspaces if workspaces else []
        self.last_workspace_id = last_workspace_id

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "workspaces": self.workspaces,
            "last_workspace_id": self.last_workspace_id
        }
