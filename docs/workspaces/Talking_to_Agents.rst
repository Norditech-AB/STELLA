Talk to Agents with the CLI
===========================

This documentation provides instructions on how to interact with Stella through the Command Line Interface (CLI). You can communicate with various agents, including a pre-installed weather agent, to get information or perform tasks.

Setting Up Your Workspace
-------------------------

**Step 1:** Connect to or Create a Workspace

   To start chatting with Stella, you need to be connected to a workspace. You can either connect to an existing workspace or create a new one.

   To connect to an existing workspace:

   .. code-block:: none

      /workspace connect <workspace_id>


   Replace ``<workspace_id>`` with the ID of the workspace you want to connect to.

   To create and connect to a new workspace:

   .. code-block:: none

      /workspace create <workspace_name>
      /workspace connect <workspace_id>


   Replace ``<workspace_name>`` with your desired workspace name and ``<workspace_id>`` with the ID of the newly created workspace.

**Step 2:** Add relevant agents to your workspace

   After connecting to your workspace, it's important to ensure that you are also add agents to it.

   Add an agent using the following command:

   .. code-block:: none

      /add <agent_id>


   Replace `<agent_id>` with the specific ID of the agent of your choice. This will establish a connection with the agent Stella can use to communicate with, allowing you to start querying information.

Chatting with the Weather Agent
--------------------------------
Chat with the pre-installed weather agent to get weather updates for any city in the world.

This agent is pre-installed in the framework, to use it, you need to explicitly add it to your workspace in order to start chatting and receiving weather updates.

   Add the weather agent using the following command:

   .. code-block:: none

      /add demo_weather_agent


   This will let Stella to communicate with the weather agent and start receiving weather information.

Once your workspace is set up and the weather agent is active, you can simply type your queries into the CLI prompt.
Here are three examples of how to ask about the weather in the three biggest cities in Sweden:

1. Asking about the weather in Stockholm:

   .. code-block:: none

      What's the weather like in Stockholm today?

2. Inquiring about the weather in Gothenburg:

   .. code-block:: none

      Can you give me the weather forecast for Gothenburg?

3. Getting weather updates for Malmö:

   .. code-block:: none

      Tell me about today's weather in Malmö.

Each of these queries will prompt the weather agent to provide current weather information or forecasts for the specified city.

Conclusion
----------

With Stella's CLI, you can easily connect to workspaces, interact with various agents, and get information or execute tasks efficiently. The pre-installed weather agent is just one example of the many functionalities available to enhance your productivity and decision-making processes.
