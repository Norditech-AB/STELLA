from .base_command import BaseCommand
import getpass


class LoginCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('login', help='Login as user')
        parser.set_defaults(command_class=LoginCommand)

    def execute(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        self.client.login(username, password)
