
class Workspace:
    def __init__(self, workspace_id, name, owner, agents=None, last_chat_id=None):
        self.id = workspace_id
        self.name = name
        self.agents = agents if agents else {}
        self.owner = owner
        self.last_chat_id = last_chat_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "agents": self.agents,
            "owner": self.owner,
            "last_chat_id": self.last_chat_id
        }