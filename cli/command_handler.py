from getpass import getpass

from cli_design import *
from tabulate import tabulate


class CommandHandler():
    def __init__(self, client):
        self.client = client

    def __call__(self, args):

        cmd = None
        arg = None
        value = None

        if len(args) == 0:
            print("No command given")
            return
        if len(args) >= 1: cmd = args[0]
        if len(args) >= 2: arg = args[1]
        if len(args) >= 3: value = args[2]
        if len(args) > 3:
            print("Too many arguments.")
            return

        if cmd == "workspace":
            if arg == "add":
                if value is None:
                    print("No workspace name given")
                else:
                    workspace_id = self.client.add_workspace()
                    self.client.rename_workspace(workspace_id, value)
            elif arg == "delete":
                self.client.workspace_delete(value)
            elif arg == "list":
                workspace_data = self.client.get_all_workspaces()
                workspace_info = [(item['_id'], item['name'], len(item['agents'])) for item in workspace_data]

                # Using tabulate to format the output
                table = tabulate(workspace_info, headers=['ID', 'Name', 'Number of Agents'], tablefmt='grid')
                print(table)
            elif arg == "switch":
                self.client.switch_workspace(value)
            else:
                print("No workspace command given")
        elif cmd == "install":
            if arg is None:
                print("No agent name given")
            else:
                self.client.install_agent(arg, value)
        elif cmd == "add":
            if arg is None:
                print("No agent name given")
            else:
                self.client.add_agent(arg)
        elif cmd == "status":
            self.__status()
        elif cmd == "set":
            if arg == "max-depth":
                if value is None:
                    print("No value given")
                else:
                    print("TODO: Set the max depth")
        elif cmd == "exit":
            print("Goodbye!")
            exit()
        elif cmd == "help" or cmd == "?":
            self.help()
        else:
            print("Unknown command. type /help for help.")

    def help(self):
        print(""" 
              Commands:
              workspace add <name>       create a new workspace
              workspace delete <name>    delete a workspace
              workspace list             list all workspaces
              workspace switch <name>    switch to a workspace
              status                     show status of agents
              exit                       exit the program
              help                       show this help
              """)

    def __status(self):

        # TODO show email in authenticated row

        workspace_data = self.client.get_workspace_by_id(self.client.workspace_id)
        if workspace_data is None:
            print("No workspace found")
            return

        # Data for the table
        headers = ["Agent", "Authenticated"]

        # Extract agent names and their authentication status
        agents = workspace_data['agents']
        rows = [[agent, 'Authenticated' if info['authorized'] else 'Unauthenticated'] for agent, info in agents.items()]

        # Apply color to specific cells
        def apply_color(cell):
            if "Authenticated" in cell:  # Check for authentication status
                return GREEN + cell + ENDC
            return cell

        # Apply color to the rows
        colored_rows = [[apply_color(cell) for cell in row] for row in rows]

        # Print the table using tabulate
        table = tabulate(colored_rows, headers=headers, tablefmt="grid")
        # workspace_name = workspace_data['workspace']['name']
        print("Using Workspace: " + VISS_GREEN + self.client.workspace_id + ENDC + "\n")
        print(table)
        print("")


if __name__ == '__main__':
    from cli.stella_client import StellaClient

    handler = CommandHandler(StellaClient())
    handler('test')
