class User:
    def __init__(self, user_id, email, password, workspaces=None):
        self.id = user_id
        self.email = email
        self.password = password
        self.workspaces = workspaces if workspaces else []

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "workspaces": self.workspaces
        }