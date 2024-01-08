Getting Started
===============

Welcome to the Quick Start Guide for STELLA! This guide will help you set up STELLA quickly and efficiently.

Prerequisites
--------------

Before you begin, ensure you have the following:

- Python 3.9 – 3.12 installed.
- Latest version of pip *(23.3.2)*
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

Step 2: Upgrade pip
-------------------
Our framework is so modern that it needs the latest and greatest pip version *(23.3.2)* to keep up! If your pip isn't this hip, it's time for an upgrade party:

.. code-block:: bash

    pip install --upgrade pip

Step 3: Install Dependencies
-----------------------------

It is now time to install the dependencies.

.. tip::
    Create a virtual environment to isolate the dependencies from other projects.
    Simply run

    .. code-block:: bash

        python -m venv venv

    to create a virtual environment named `venv` in the current directory.

    Then on MacOS/Unix run:

    .. code-block:: bash

        source venv/bin/activate

    or on Windows:

    .. code-block:: bash

        venv\Scripts\activate

    to activate the virtual environment.


Install dependencies by running the following command from the project directory:

.. code-block:: bash

    pip install -e .

.. note:: make sure to use the -e flag to install the dependencies in editable mode. This will allow you to make changes to the code and have them reflected in the installed package.

Optional: Install Development Dependencies (for contributors)
    .. code-block:: bash

        pip install -e ".[dev]"

Step 4: Setup the Environment
-----------------------------

Setup the Environment by running the :file:`configure.py` script from the root folder:
This will walk you through the setup process and create a `.env` file in the root directory.

.. code-block:: bash

    stella configure.py

You need an api key from OpenAI to use the agent. Read more about how to get one `here <https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key>`_ and paste it into the prompt.

Step 4: Start the Server
-------------------------

With the environment configured, start the server by running `stella serve`:

.. code-block:: bash

    stella serve

.. seealso:: If you encounter issues starting the server, refer to the :doc:`Troubleshooting` guide for common problems and solutions.

Step 5: Explore and create in the CLI
--------------------------------------
Open a **new terminal window** and run `stella` to move into the CLI. This will open a Python shell with the STELLA environment loaded. You can now explore the framework and create your own agents.

.. code-block:: bash

    stella

Step 6: Register your account and start chatting
--------------------------------------------------

Create and configure your workspace using the CLI:

1. **Register:**

   .. code-block:: bash

       /register

Enter your username and password to register your account.

.. note:: This data is stored in your local database and is not shared with anyone.

2. **Start chatting with STELLA:**

Now you are ready to start chatting with STELLA. The default Weather agent is already installed so you can start chatting with it right away by firstly adding it to your workspace:

   .. code-block:: bash

       /add demo_weather_agent

Lets see what the weather is like in Stockholm as an example:

   .. code-block:: bash

       What is the weather in Stockholm?

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

