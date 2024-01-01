from .base_command import BaseCommand


class WorkspaceCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        workspace_parser = subparsers.add_parser('workspace', help='Workspace operations')
        workspace_subparsers = workspace_parser.add_subparsers(dest='workspace_command')

        # Add workspace subcommands here

        # Create workspace subcommand
        parser_add = workspace_subparsers.add_parser('create', help='Create workspace')
        parser_add.add_argument('workspace_name', help='Name of the workspace to add')
        parser_add.set_defaults(workspace_command_class=WorkspaceCommand)

        #

    def execute(self):
        # Logic to handle different workspace commands
        if self.args.workspace_command == 'create':
            self.client.create_workspace(self.args.workspace_name)
