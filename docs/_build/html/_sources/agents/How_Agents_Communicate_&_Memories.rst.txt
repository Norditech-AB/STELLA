Agent Communication and Task Execution
=======================================

This documentation provides an in-depth look at how agents in our framework communicate with each other and execute tasks, with a focus on the `Task` class's role in this process.

Agent Communication Overview
----------------------------

Agents communicate by sending and receiving a `Task` object. The `Task` object is central to the decision-making process in action selection and determining the completion status of a task. This process involves evaluating the user's input (chat query) and the information accumulated in the task's memories from previous agent interactions.

Task Execution Workflow
-----------------------

The `Task` class's `execute` method outlines the workflow for task execution:

1. **Loading the Current Agent:**
   The agent responsible for the current task is loaded.

2. **Action Selection:**
   The agent evaluates the current situation based on the chat history and memories and then selects an appropriate action.

3. **Handling Subtasks or Completion:**
   Depending on the action selected, the task may be passed to another agent (subtask creation) or marked as complete.

4. **Updating and Forwarding Task Memories:**
   The task's memories are updated with new information. If the task is complete, it is passed back to the parent agent.

Example: Task Execution in DemoWeatherAgent
--------------------------------------------

Below is a detailed example from the `DemoWeatherAgent` that showcases the task execution process:

.. code-block:: python

    def execute(self, agent_storage, openai_client, socketio, request_builder):
        # [Initial setup and context retrieval]
        # ...

        # Load the current agent
        current_agent = agent_storage.load(self.current_agent)

        # Check for max depth
        # ...

        # Perform action selection
        # ... (Action selection logic using chat and memories)
        # Selected action is determined here

        # Action handling
        if selected_action != "0":
            # Create a new task for the selected agent
            # ... (Code for creating and returning a new task)
        elif selected_action == "0":
            # Handle task completion
            # ... (Code for generating a response, updating memories, and handling top-level or subtasks)

Understanding Task Flow and Agent Interaction
----------------------------------------------

1. **Loading Agents:**
   The executing agent, identified by `current_agent`, is loaded from the `agent_storage`. This agent now has the context and is ready to make decisions.

2. **Depth Check:**
   Before proceeding, the agent checks if the maximum depth of query handling has been reached. This prevents overly complex or circular queries.

3. **Building the Action Map:**
   The agent constructs an action map that represents potential actions or sub-agents to delegate the task to.

4. **Selecting an Action:**
   The agent uses the chat history, current task memories, and the action map to select the best course of action.

5. **Delegating or Completing the Task:**
   If another agent is selected, a new task for that agent is created. If the action selection returns "0", it indicates that the agent considers the task complete.

6. **Updating and Forwarding Memories:**
   The task's memories are updated with new information or completion status. These memories are crucial for maintaining the context and history of the interaction.

.. note::
   Agent Memory Attributes
   ------------------------------

   Agents can be pre-configured with the following attributes to control their interaction with task memories:

   - **wants_memories (bool = True):**
     This attribute determines whether the agent wants to access the task's memory. When set to `True`, the agent considers the accumulated memories in its decision-making process.

   - **forward_all_memory_entries_to_parent (bool = False):**
     If set to `True`, the agent will forward all memory entries to its parent task upon completion. This is useful when the parent task needs to maintain a full context of the child task's activities and decisions.

   - **forward_last_memory_to_parent (bool = False):**
     When this attribute is `True`, only the last entry in the task's memories is forwarded to the parent task. This option is beneficial when only the final outcome or decision of the child task is relevant to the parent.

   For more information on agent attributes, see the :doc:`The_Agent_Class` documentation.

These attributes provide flexibility in how agents handle and transmit information within the task framework, allowing for more tailored and efficient agent behaviors.


Conclusion
----------

Through the `Task` class and its execution method, our framework provides a structured way for agents to interact, make decisions, and pass on information. This system allows for the creation of complex, multi-agent workflows that can handle intricate user queries and tasks.
