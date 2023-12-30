import argparse
from cli.stella_client import StellaClient
from cli.command_handler import CommandHandler
import getpass  # For securely prompting for a password
from shell import Shell
from cli_design import *
from sanitization import Sanitization


def print_examples():
    print("""
        start backend server:   stella serve
        configure project:      stella config
        check project:          stella doctor

        login as user:          stella login
        logut as user:          stella logout
        register user:          stella register

        list workspaces:        stella workspace list
        add workspace:          stella workspace add myworkspace
        delete workspace:       stella workspace delete myworkspace
        switch workspace:       stella workspace switch defaultWorkspace

          
        add agent to ws:        stella add spotify
        remove agent from ws:   stella remove spotify
        authenticate agent:     stella auth spotify 
          
        install agent:          stella install spotify
        uninstall agent:        stella uninstall spotify
        update agent:           stella update spotify
        search for agents:      stella search spotify

        list all agents:        stella status
        stella clean            clean history in chat         
        chat with agents:       stella
    """)

def main():
    client = StellaClient()

    parser = argparse.ArgumentParser(description="Stella Command Line Interface")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    help = subparsers.add_parser('help', help='Show help')

    # Server command
    parser_serve = subparsers.add_parser('serve', help='Start backend server')
    parser_serve.add_argument('--host', help='Host to run the server on', default='localhost')
    parser_serve.add_argument('--port', help='Port to run the server on', default=5001)

    # User commands
    parser_login = subparsers.add_parser('login', help='Login as user')
    #parser_login.add_argument('username', help='Username for login')

    parser_logout = subparsers.add_parser('logout', help='Logout as user')

    config = subparsers.add_parser('config', help='Configure project')

    parser_register = subparsers.add_parser('register', help='Register user')

    # Workspace commands
    parser_workspace = subparsers.add_parser('workspace', help='Workspace operations')
    workspace_subparsers = parser_workspace.add_subparsers(dest='workspace_command')

    parser_workspace_list = workspace_subparsers.add_parser('list', help='List workspaces')
    parser_workspace_add = workspace_subparsers.add_parser('add', help='Add workspace')
    parser_workspace_add.add_argument('workspace_name', help='Name of the workspace to add')

    parser_workspace_delete = workspace_subparsers.add_parser('delete', help='Delete workspace')
    parser_workspace_delete.add_argument('workspace_name', help='Name of the workspace to delete')

    parser_workspace_switch = workspace_subparsers.add_parser('switch', help='Switch workspace')
    parser_workspace_switch.add_argument('workspace_name', help='Name of the workspace to switch to')

    parser_install = subparsers.add_parser('install', help='Install agent')
    parser_install.add_argument('agent_name', help='Name of the agent to install')
    parser_install.add_argument('version', help='Version of the agent to install', default='latest', nargs='?')

    # Agent commands
    parser_status = subparsers.add_parser('status', help='List all agents')

    parser_auth = subparsers.add_parser('auth', help='Authenticate agent')
    parser_auth.add_argument('agent_name', help='Name of the agent to authenticate')

    parser_add = subparsers.add_parser('add', help='Add agent')
    parser_add.add_argument('agent_name', help='Name of the agent to add')

    parser_chat = subparsers.add_parser('chat', help='Chat with agents')

    parser_version = subparsers.add_parser('version', help='Show version')
    larser_examples = subparsers.add_parser('examples', help='Show examples')

    args = parser.parse_args()
    cmd_list = sys.argv[1:]

    if args.command == 'serve':
        import os
        os.chdir('../app')
        # Base command for running the server
        server_command = 'python3 run.py'

        # Add host and port to the command only if they are provided
        if args.host:
            server_command += f' --host {args.host}'
        if args.port:
            server_command += f' --port {args.port}'

        # Run the server with the constructed command
        os.system(server_command)
        
    elif args.command == 'config':
        Sanitization().configure_project()
        return

    elif args.command == 'login':
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        client.login(username, password)
        return

    elif args.command == 'register':

        username = input("Username: ")
        password = getpass.getpass("Password: ")
        client.register(username, password)
    
    if not client.is_authenticated():
        print("Not logged in, try " + VISS_GREEN + "stella login" + ENDC)
        exit(0)
        #print("Authenticated as", client.get_username())

    if args.command is None:
        shell = Shell(client)
        shell.cmdloop()
    else:
        CommandHandler(client)(cmd_list)


if __name__ == '__main__':
    main()
    #start_server()
