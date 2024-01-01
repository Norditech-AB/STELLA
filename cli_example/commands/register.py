from .base_command import BaseCommand
import getpass


class RegisterCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('register', help='Register user')
        parser.set_defaults(command_class=RegisterCommand)

    def execute(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        self.client.register(username, password)
