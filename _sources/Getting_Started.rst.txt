Getting Started
===============

Welcome to the Quick Start Guide for STELLA! This guide will help you set up STELLA quickly and efficiently.

Prerequisites
--------------

Before you begin, ensure you have the following:

- Python 3.9 – 3.10 installed.
- Git installed for cloning the repository.
- Basic familiarity with command-line operations.

Step 1: Clone the Repository
----------------------------

Clone the STELLA repository using your preferred method:

**HTTPS:**

.. code-block:: bash

    git clone https://github.com/Norditech-AB/STELLA.git

**SSH:**

.. code-block:: bash

    git clone git@github.com:Norditech-AB/STELLA.git

**GitHub CLI:**

.. code-block:: bash

    gh repo clone Norditech-AB/STELLA

Step 2: Install Dependencies
-----------------------------

Before running the server, install any necessary dependencies:

.. code-block:: bash

    pip install -r requirements.txt

.. tip::
    Create a virtual environment to isolate the dependencies from other projects.
    Simply run

    .. code-block:: bash

        python3 -m venv venv

    to create a virtual environment named `venv` in the current directory.

    Then on MacOS/Unix run:

    .. code-block:: bash

        source venv/bin/activate

    or on Windows:

    .. code-block:: bash

        venv\Scripts\activate

    to activate the virtual environment.

    Now, install the dependencies by running:

    .. code-block:: bash

        pip install -r requirements.txt

    More information on virtual environments can be found in the `Python documentation <https://docs.python.org/3/tutorial/venv.html>`_.

Step 3: Setup the Environment
-----------------------------

Setup the Environment by running the :file:`configure.py` script from the root folder:
This will walk you through the setup process and create a `.env` file in the root directory.

.. code-block:: bash

    python configure.py

Step 4: Start the Server
-------------------------

With the environment configured, start the server by running `python stella serve` script from the root folder:

.. code-block:: bash

    python stella serve

.. seealso:: If you encounter issues starting the server, refer to the :doc:`Troubleshooting` guide for common problems and solutions.

Step 5: Explore and create in the CLI
--------------------------------------
Open a new terminal window and run `python stella` from the `root` folder of the repository to move into the CLI. This will open a Python shell with the STELLA environment loaded. You can now explore the framework and create your own agents.

.. code-block:: bash

    python stella

Step 6: Create Your Account and Workspace
------------------------------------------

Create and configure your workspace using the CLI:

1. **Register:**

   .. code-block:: bash

       /register

2. **Login:**

Login with your newly created account:

   .. code-block:: bash

       /login

3. **Create a Workspace:**

Create a workspace to start chatting with STELLA. Replace `<workspace_name>` with the name of your workspace or leave it blank:

   .. code-block:: bash

       /workspace create <workspace_name>

4. **Start chatting with STELLA:**

Now you are ready to start chatting with STELLA. The default Weather agent is already installed so you can start chatting right away:

Lets see what the weather is like in Jönköping as an example:

   .. code-block:: bash

       What is the weather in Jönköping?

.. note:: Add agents to your workspace (replace `<agentid>` with the actual agent ID):

   .. code-block:: bash

       /add <agentid>

.. note:: Use the /help command to see all available commands:

   .. code-block:: bash

       /help


Step 7 (OPTIONAL): Configure the .env File
-------------------------------------------

To customize your STELLA environment, you can update the `.env` file in the root directory. This file contains all the environment variables used by STELLA.
Navigate to the STELLA directory and update the `.env` file with your information:

.. code-block:: none

    JWT_SECRET_KEY="<REPLACE ME>"
    BCRYPT_SALT="<REPLACE ME>"
    MONGO_USERNAME="<REPLACE ME>"
    MONGO_PASSWORD="<REPLACE ME>"
    MONGO_URI="<REPLACE ME>"
    MONGO_DB="<REPLACE ME>"
    OPENAI_API_KEY="<REPLACE ME>"
    FLASK_CONFIG="development"
    JWT_ACCESS_TOKEN_EXPIRES="7"
    SOCK_SERVER_OPTIONS_PING_INTERVAL="150"
    ASYNC_MODE="gevent"

Each placeholder should be replaced with your specific values. For instance, `OPENAI_API_KEY` requires a valid API key from OpenAI.

.. tip:: Visit the :doc:`configuration/Environment_Variables` section for detailed guidance on setting up each variable.

.. note:: The `FLASK_CONFIG` variable is set to `development` by default. This is not recommended for production environments.

Next Steps
----------

Congratulations on setting up STELLA! Now, you're ready to dive deeper:

- Explore more default agents provided in :file:`/app/agents/DefaultAgents` to get a feel for STELLA's capabilities.
- Learn how to create your first agent in the :doc:`agents/Creating_a_new_Agent` guide.
- Explore advanced CLI commands in the :doc:`cli/index` section.

