Creating a new User
===================

This section details the process of creating a new user in our framework through the Command Line Interface (CLI).

Overview
--------

Creating a new user is a simple process that can be done directly from the CLI. The user's information, including email and password, will be securely stored in the connected database.

Database Storage
----------------

When a new user is created:

- **Email**: The user's email address is stored as a unique identifier.
- **Password**: The password is securely hashed and stored. We ensure the security of user passwords by using robust hashing algorithms.

Creating a User via CLI
-----------------------

To create a new user, follow these steps:

1. **Open the CLI**:
   Start by opening the CLI environment. Ensure that you are in the root directory of the framework.

2. **Run the Registration Command**:
   Use the registration command to initiate the user creation process. You will be prompted to enter the user's email and password.

   Example Command:

   .. code-block:: bash

       /register

3. **Enter User Details**:
   - When prompted, enter the user's **email address**.
   - Next, enter the **password** for the new account.

   The CLI will communicate with the backend to create the user and store the details in the database.

Success Confirmation
--------------------

Upon successful creation of the new user, you will receive a confirmation message in the CLI indicating that the user account has been created.

Handling Errors
---------------

If there are any issues during the user creation process, such as entering an already existing email, the CLI will display an appropriate error message. Follow the instructions provided in the error message to resolve the issue.

More Details
------------

For more details on the create user endpoint, refer to the :doc:`../API_Reference` documentation.

Conclusion
----------

Creating a new user through our CLI is a straightforward process. Once created, the user's details are securely stored in the database, ensuring the safety and integrity of user data.
