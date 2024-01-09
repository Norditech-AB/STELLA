How Agents Communicate & Memories
=================================

In Stella, agents are the autonomous units capable of performing specialized tasks designed to simulate the behavior of an assistant. Communications between agents are central to creating cohesive and intelligent responses to user requests and handling complex tasks that require collaboration. This documentation provides a detailed explanation of agent communication, the use of memories, and the task execution flow within the Stella system.


Agent Communication
-------------------

Agents communicate by passing information through tasks. Each task can invoke subtasks, and agents can use memories to share information and context:

- **Task Inception**: A task is initiated when a user interacts with Stella, often through a chat interface. This top-level task is then managed by a coordinator agent.

- **Action Selection**: Each agent is responsible for deciding whether to handle a request or delegate it to another agent. This process decides the direction of information flow and task allocation.

- **Subtasks**: If an agent determines that another agent is better suited for the task or a subset thereof, it can create a subtask with a new agent in charge.

- **Memories**: Agents retain and share memories, valuable information and context from their interactions. These memories are propagated to the parent task upon subtask completion, if configured to do so.


Memories
--------

Memories are akin to notes that agents keep during their processes. They record useful details that can help in ongoing and future tasks:

- **Persistent Context**: Memories are persisted across tasks and subtasks, maintaining context and avoiding repetitive queries.

- **Sharing Knowledge**: Agents can choose to transfer all or part of their memories to parent tasks, enabling higher-level agents to access the accumulated knowledge.

- **Customizable Propagation**: The behavior of memory propagation—either all memory entries or only the last one—can be customized for each agent.


Tasks and Task Execution
------------------------

Tasks are discrete units of work delegated to agents. The task execution mechanism is integral to Stella's operation:

- **Task Initialization**: Upon receiving a user request, a top-level task is created.

- **Execution Flow**: The task is then executed in a sequence that might involve action selection, subtask creation, or generation of a response.

- **Subtask Communication**: Subtasks can communicate with their parent task by transferring memories or signals upon completion.


Task Execution Flow
-------------------

Here is an in-depth look at the task execution process:

1. **Load Current Agent**: The current agent, responsible for handling the task, is loaded from the Agent Storage.

2. **Action Selection**:

   - **Analyzing Options**: The agent uses action selection to evaluate which agent or action, available in the action map, is best suited to handle the request.
   - **Decision Making**: If the agent selects itself or decides that no further action is needed, it will generate a response.

3. **Subtask Generation**:

   - If an agent other than the current one is selected during action selection, a new subtask is created, and control is transferred to the chosen agent.

4. **Task Execution**:

   - **Subtasks**: For subtasks, upon completion, they can send memories back to the parent task.
   - **Top-Level Tasks**: When the top-level task is completed, it generates a response back to the user.

5. **Task Completion**:

   - A task is marked as completed once it has either generated a response or created a subtask that is now responsible for continuing the task execution flow.


Agent Max Depth
---------------

Each agent has an attribute defining its maximum subtask depth to prevent circular task delegations and ensure manageable complexity. The system enforces this by tracking the depth of each subtask:

- **Global Limit**: There is a global setting for maximum task depth, preventing the over-complication of conversations.
- **Agent-Specific Limit**: Individual agents may have specific maximum depth settings to constrain their operation complexity.

On task execution, the depth is checked—if a task reaches its maximum depth, a warning is sent to the user without proceeding further.

.. note::

   The depth attribute guides the system in maintaining performance and preventing infinite loops or excessive delegation.
