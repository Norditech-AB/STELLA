from getpass import getpass

from cli.client.stella_client import StellaClient

from cli.client.cli_design import *
from cli.client.cli_design import *

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

import os


AVAILABLE_COMMANDS = """Available commands:

    /login                                      login as user
    /logout                                     logout as user
    /register                                   register user
    
    /username <new username>                    change username
    /password <old password> <new password>     change password
    
    /workspace create <name>                    create workspace
    /workspace list                             list workspaces
    /workspace connect <id>                     switch workspace
    /workspace rename <id> <name>               rename workspace
    /workspace delete <id>                      delete workspace
    /status                                     show workspace status
    
    /add <agent id>                             add agent to workspace
    /remove <agent id>                          remove agent from workspace
    /coordinator <agent id>                     set workspace coordinator
    
    /install <agent id>                         install agent in repository
    
    /exit                                       exit the program
"""



class Shell:
    def __init__(self, client: StellaClient):
        self.client: StellaClient = client
        self.version = "0.1.0"
        self.active = True
        self.authenticated = False
        self.prompt_session = PromptSession(history=InMemoryHistory())

    def motd(self):
        print("\n\n")
        print_banner()
        print(f"     CLI v{self.version}\n")

    def start(self):

        connection_available = self.client.verify_connection()
        if not connection_available:
            print_error(f"Could not connect to STELLA server ({self.client.compose_url('')}).")
            print_info("Verify that the STELLA server is running and that the CLI configuration `stella/config.json` "
                       "file matches the server configuration.")
            print_info("Start the server by running `stella serve` from the root directory of the project.")
            exit(1)

        # Check if the user is logged in
        self.authenticated = self.client.is_logged_in()

        # If not, ask the user to login or register
        if not self.authenticated:
            # Show message of the day (welcome message)
            self.motd()
            print('\n')
            try:
                while not self.authenticated:
                    print_info("Please login or register to continue.")
                    print_info("Type /login to login or /register to create a new account.")
                    command = input(" > ")

                    if command.strip().lower() == '/login':
                        self.execute('login')
                    elif command.strip().lower() == '/register':
                        self.execute('register')

                    self.authenticated = self.client.is_logged_in()
            except KeyboardInterrupt:
                self.shutdown()

        # Show message of the day (welcome message) + info
        user = self.client.get_user()
        self.motd()
        print(f" > Welcome {user['username']}. How can I help you today?\n")
        print_success(f"Connected to STELLA server running on {self.client.compose_url('')}.")
        print_info("To chat with agents, type a message and press enter. (do not start with '/')")
        print(f"Type /help to list commands.\n")

        # Connect to the latest workspace and chat, if any
        self.client.connect_latest()

        # Once authenticated, proceed to the main loop
        try:
            while self.active:
                if not self.client.waiting_for_response:
                    message = self.prompt_session.prompt(' > ')

                    # Check if command or message
                    if message.startswith('/'):
                        self.execute(message[1:])
                    else:
                        self.chat(message)
                else:
                    while self.client.waiting_for_response:
                        time.sleep(0.01)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.active = False
        print("\n")
        print_info("STELLA CLI Shutting down... See you next time!")
        os._exit(0)  # Exit without throwing an exception, to avoid printing the stack trace

    def execute(self, command):
        # Split the command into a list of arguments
        args = command.split(' ')

        # If the command is 'exit', exit the shell
        if args[0] == 'exit':
            exit(0)
        elif args[0] == 'login':
            username = input("Username: ")
            password = getpass("Password: ")
            self.client.login(username, password)
            return
        elif args[0] == 'logout':
            self.client.logout()
            return
        elif args[0] == 'register':
            username = input("Username: ")
            password = getpass("Password: ")
            confirm_password = getpass("Confirm password: ")

            if password != confirm_password:
                print_error("Passwords do not match.")
                return

            try:
                self.client.register(username, password)
            except Exception as e:
                print_error(str(e))
                return None

            try:
                self.client.login(username, password)
            except Exception as e:
                return None

            try:
                workspace_id = self.client.create_workspace()
            except Exception as e:
                return None

            if workspace_id:
                self.client.connect_to_workspace(workspace_id)
            return
        elif args[0] == 'username':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                self.client.change_username(args[1])
                return
        elif args[0] == 'password':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                confirm_password = getpass("Confirm new password: ")

                if args[1] != confirm_password:
                    print_error("Passwords do not match.")
                    return

                self.client.change_password(args[1])
                return

        elif args[0] == 'workspace' or args[0] == 'ws':
            # If the user only typed '/workspace', show the current workspace status
            if len(args) == 1:
                try:
                    workspace = self.client.get_workspace_by_id(self.client.session.workspace_id)
                except Exception as e:
                    print_error("You are not connected to a workspace. Type /help for a list of commands.")
                    return
                pretty_print_workspace(workspace)
            elif args[1] == 'create':
                # If the user passed a name, also include this in the method call
                if len(args) == 3:
                    workspace_id = self.client.create_workspace(name=args[2])
                else:
                    workspace_id = self.client.create_workspace()
                if workspace_id:
                    self.client.connect_to_workspace(workspace_id)
                return
            elif args[1] == 'rename':
                if len(args) == 3:
                    self.client.rename_workspace(args[2])
                else:
                    print_info("Missing argument. Type /help for a list of commands.")
                return
            elif args[1] == 'list':
                workspaces = self.client.get_all_workspaces()
                if not workspaces:
                    return
                pretty_print_workspaces(workspaces)
                return
            elif args[1] == 'connect':
                if len(args) == 2:
                    print_info("Missing argument. Type /help for a list of commands.")
                    return
                else:
                    self.client.connect_to_workspace(args[2])
                return
            elif args[1] == 'delete':
                self.client.delete_workspace(args[2])
                return
            else:
                print_error("Unknown Workspace command. Type /help for a list of commands.")
                return
        elif args[0] == 'add':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                self.client.add_agent(args[1])
                return
        elif args[0] == 'remove':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                self.client.remove_agent(args[1])
                return
        elif args[0] == 'coordinator':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                self.client.set_coordinator_agent(args[1])
                return
        elif args[0] == 'install':
            if len(args) == 1:
                print_info("Missing argument. Type /help for a list of commands.")
                return
            else:
                self.client.install_agent(args[1])
                return
        elif args[0] == 'status':
            try:
                workspace = self.client.get_workspace_by_id(self.client.session.workspace_id)
            except Exception as e:
                print_error("You are not connected to a workspace. Type /help for a list of commands.")
                return
            pretty_print_workspace(workspace)
            return
        elif args[0] == 'help':
            print(AVAILABLE_COMMANDS)
            print_info('For more information, visit https://docs.stellaframework.com/')
            print_info("To chat with agents, type a message and press enter. (do not start with '/')")
        else:
            print_error('Unknown command. Type /help for a list of commands.')

    def chat(self, message):
        if self.client.waiting_for_response:
            return
        try:
            self.client.send_message(message)
        except Exception as e:
            print_error(f"You are not connected to a workspace. Type /help for a list of commands.")
            return