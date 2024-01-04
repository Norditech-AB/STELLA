Managing Workspaces in the CLI
==============================

This section provides guidance on managing workspaces in our framework via the Command Line Interface (CLI). Workspaces in our framework serve as hubs for collaboration and automation across various applications.

Overview
--------

Workspaces are central to organizing and managing your activities within the framework. They allow for the integration of agents and automation tools, facilitating a collaborative and efficient environment. Workspaces, including their configurations and associated agents, can be shared or exported to the marketplace for Stella workspaces.

.. tip::
    You can use ``/ws`` as a shortcut for ``/workspace`` in the CLI.

What is a Workspace?
--------------------

A workspace in our framework is a virtual environment or hub where users can manage and interact with various components like agents and automated processes.
It serves as a container for different tasks and projects, providing a structured environment for managing activities related to Stella workspaces.
Each workspace can be tailored with specific agents and tools to fit the unique needs of a project or team.

Creating a Workspace
--------------------

To create a new workspace:

1. Enter the command:

   .. code-block:: none

      /workspace create <workspace_name>

   Replace ``<workspace_name>`` with your desired workspace name. If no name is specified, a default name like "Untitled Workspace" is assigned.

2. The newly created workspace will be stored in the connected database with its configuration details.

Viewing Workspaces
------------------

To view all your workspaces:

1. Enter the command:

   .. code-block:: none

      /workspace list

   This command will list all workspaces associated with your user account.

Connect to a Specific Workspace
-------------------------------

To connect to a specific workspace:

1. Enter the command:

   .. code-block:: none

      /workspace connect <workspace_id>

   Replace ``<workspace_id>`` with the ID of the workspace you want to view. This command provides detailed information about the specified workspace.

Renaming a Workspace
--------------------

To rename an existing workspace:

1. Enter the command:

   .. code-block:: none

      /workspace rename <workspace_id> <new_name>

   Replace ``<workspace_id>`` with the ID of the workspace you want to rename, and ``<new_name>`` with the new name for the workspace.

2. The workspace's name will be updated in the database.

Adding an Agent to a Workspace
-------------------------------

**Quick Steps to Connect an Agent to Your Workspace:**

**Step 1:** Connect to Your Workspace

   Begin by establishing a connection to the workspace. Do this by typing the command:

   .. code-block:: none

      /workspace connect <workspace_id>

   Replace ``<workspace_id>`` with the actual ID of the workspace you want to connect to.

**Step 2:** Add an Agent

   Once connected, you can add an agent to this workspace. Simply enter:

   .. code-block:: none

      /add <agent_id>

   Replace ``<agent_id>`` with the ID of the agent you wish to add.

Removing an Agent from a Workspace
-----------------------------------

**Simple Guide to Remove an Agent from Your Workspace:**

To disassociate an agent from a workspace, follow these steps:

1. Begin by Establishing a Connection to the Workspace:

   First, ensure you are connected to the workspace from which you want to remove an agent. Once connected, proceed to the next step.

2. Enter the Remove Agent Command:

   Use the command to remove an agent:

   .. code-block:: none

      /remove <agent_id>

   Replace ``<agent_id>`` with the ID of the agent you wish to remove.

3. Confirmation of Removal:

   After executing the command, the specified agent will be successfully removed from the workspace.

Deleting a Workspace
--------------------

To delete a workspace:

1. Enter the command:

   .. code-block:: none

      /workspace delete <workspace_id>

   Replace ``<workspace_id>`` with the ID of the workspace you wish to delete.

2. The workspace and all its associated data will be removed from the database.

Conclusion
----------

Workspaces are a versatile and integral part of our framework, enabling users to manage and collaborate efficiently. Through the CLI, users can easily create, configure, and interact with workspaces, tailoring them to their specific needs and workflows.
