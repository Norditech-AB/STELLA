class User:
    def __init__(self, user_id, email, password, workspaces=None, last_workspace_id=None):
        self.id = user_id
        self.email = email
        self.password = password
        self.workspaces = workspaces if workspaces else []
        self.last_workspace_id = last_workspace_id

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "workspaces": self.workspaces,
            "last_workspace_id": self.last_workspace_id
        }
