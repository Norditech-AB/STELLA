The Agent Class
===============

The ``Agent`` superclass is a fundamental part of our framework, defining the core functionalities and attributes of an agent. This document provides a detailed overview of the ``Agent`` class and its key components.

Class Overview
--------------

The ``Agent`` class is designed to load and store information about an agent. It includes various attributes and methods that dictate how an agent behaves, interacts, and makes decisions in the framework.

Attributes
----------

The following are the key attributes of the ``Agent`` class:

- **agent_id (str):**
  A unique identifier for the agent.

- **name (str):**
  The name of the agent.

- **short_description (str):**
  A brief description of what the agent does.

- **model_for_action_selection (str, default='gpt-4'):**
  The model used by the agent for selecting actions.

- **model_for_response (str, default='gpt-4'):**
  The model used by the agent for generating responses.

- **wants_chat (bool, default=True):**
  Indicates whether the agent requires chat history for its operations.

- **wants_memories (bool, default=True):**
  Determines if the agent needs access to the task's memories.

- **forward_all_memory_entries_to_parent (bool, default=False):**
  If set to True, the agent forwards all memory entries to its parent after completing its task.

- **forward_last_memory_to_parent (bool, default=False):**
  If True, only the last memory entry is forwarded to the parent agent.

- **system_action_selection_instructions (str):**
  Default instructions for the agent to follow during action selection.

- **system_response_instructions (str):**
  Default instructions for generating responses to user queries.

- **done_condition (str):**
  The condition that defines when a user's task has been completed.

- **skip_response (bool, default=False):**
  Determines whether to skip the response generation phase.

- **skip_action_selection (bool, default=False):**
  Indicates whether to bypass the action selection process.

- **connections_forced (dict, default=None):**
  Specifies connections that are forcefully established with other agents.

- **connections_available (dict, default=None):**
  A dictionary defining available connections to other agents.

- **max_depth (int, default=None):**
  The maximum depth an agent can reach in a task hierarchy.

Key Methods
-----------

The ``Agent`` class includes several important methods:

- **select_action:**
  This method allows the agent to choose an action based on the current context, chat history, and memories.

- **respond:**
  Generates a response to the user's request using the provided details and context.

- **_construct_memory_string:**
  A static method to construct a string representation of the available memories.

- **_construct_chat_string:**
  A static method to construct a string representation of the chat history with the user.

- **_construct_available_actions_string:**
  Builds a string representation of the available actions an agent can take.

Usage Example
-------------

.. code-block:: python

    class DemoAgent(Agent):
        def __init__(self):
            super().__init__(
                agent_id="demo_agent",
                name="Demo Agent",
                short_description="Demonstration agent",
                # Other attributes...
            )

Conclusion
----------

The ``Agent`` superclass provides a comprehensive framework for creating and managing agents. Its attributes and methods enable flexible and sophisticated interactions within the system, allowing agents to make informed decisions and respond effectively to user queries.
