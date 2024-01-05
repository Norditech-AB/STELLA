import os
import importlib.util

from app.models.agent import Agent


class AgentStorage:
    """
    Loads and stores information about all agents, including those in subdirectories.
    """
    agents = {}

    def __init__(self):
        self._load_agents()

    def _load_agents(self):
        print("Loading agents...")

        # Define the path to the agents directory
        agents_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agents')

        # Call the recursive function to load agents
        self._load_agents_recursive(agents_dir)

        print(f"Loaded agents: {self.agents}")

    def _load_agents_recursive(self, directory):
        """ Recursively load agents from the given directory and its subdirectories. """
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)

            if os.path.isdir(full_path):
                # If it's a directory, recursively load agents from it
                self._load_agents_recursive(full_path)
            elif entry.endswith('.py') and entry != '__init__.py':
                # Load the agent from the Python file
                self._load_agent_from_file(full_path, entry)

    def _load_agent_from_file(self, file_path, filename):
        """ Load an agent from a Python file. """
        # Generate a module name based on the filename
        module_name = filename[:-3]

        # Load and import the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Iterate over all attributes in the module
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            # If the attribute is a class, is a subclass of Agent, and isn't Agent itself
            if isinstance(attribute, type) and issubclass(attribute, Agent) and attribute != Agent:
                # Instantiate the agent and add to the storage
                agent_instance = attribute()
                self.agents[agent_instance.agent_id] = agent_instance

    def load(self, agent_id: str):
        return self.agents.get(agent_id, None)

    def reload(self):
        self.agents = {}
        self._load_agents()

    def __getitem__(self, key: str) -> 'Agent':
        return self.agents[key]

    def __iter__(self):
        return iter(self.agents.values())

    def __len__(self):
        return len(self.agents)
