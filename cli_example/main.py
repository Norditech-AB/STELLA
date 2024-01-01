import argparse
from client.stella_client import StellaClient
from commands import (ServeCommand, LoginCommand, LogoutCommand, RegisterCommand,
                      WorkspaceCommand, #StatusCommand, AuthCommand, AddCommand,
                      #ChatCommand, ExamplesCommand
                      )
from utils.examples import print_examples


def setup_parser():
    parser = argparse.ArgumentParser(description="Stella Command Line Interface")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    ServeCommand.init_parser(subparsers)
    LoginCommand.init_parser(subparsers)
    LogoutCommand.init_parser(subparsers)
    RegisterCommand.init_parser(subparsers)
    WorkspaceCommand.init_parser(subparsers)
    #StatusCommand.init_parser(subparsers)
    #AuthCommand.init_parser(subparsers)
    #AddCommand.init_parser(subparsers)
    #ChatCommand.init_parser(subparsers)
    #ExamplesCommand.init_parser(subparsers)

    return parser


def main():
    client = StellaClient()
    parser = setup_parser()
    args = parser.parse_args()

    if args.command:
        command = args.command_class(client, args)
        command.execute()
    else:
        print_examples()


if __name__ == '__main__':
    main()
