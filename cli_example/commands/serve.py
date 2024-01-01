from .base_command import BaseCommand
import os


class ServeCommand(BaseCommand):
    @staticmethod
    def init_parser(subparsers):
        parser = subparsers.add_parser('serve', help='Start STELLA server')
        parser.add_argument('--host', help='Host to run the server on', default='localhost')
        parser.add_argument('--port', help='Port to run the server on', default=5001)
        parser.set_defaults(command_class=ServeCommand)

    def execute(self):
        os.chdir('../app')
        server_command = f'python3 run.py --host {self.args.host} --port {self.args.port}'
        os.system(server_command)
