from .base_command import BaseCommand


class LogoutCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('logout', help='Logout as user')
        parser.set_defaults(command_class=LogoutCommand)

    def execute(self):
        self.client.logout()
