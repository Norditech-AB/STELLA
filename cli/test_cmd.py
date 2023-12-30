import cmd

class MyShell(cmd.Cmd):
    intro = 'Welcome to my shell. Type help or ? to list commands.\n'
    prompt = '(myshell) '

    def do_greet(self, arg):
        print(f"Hello, {arg}!")

    def do_exit(self, arg):
        print("Goodbye!")
        return True
    def emptyline(self):
        # Override the method to do nothing on an empty line
        pass

if __name__ == '__main__':
    MyShell().cmdloop()
