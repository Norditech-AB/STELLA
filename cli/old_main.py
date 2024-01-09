import os
import sys

def init():

    def add_current_directory_to_pythonpath():
        # Get the directory where the script is run from
        current_directory = os.getcwd()

        # Get the current PYTHONPATH
        current_pythonpath = os.environ.get('PYTHONPATH', '')

        # Construct the new PYTHONPATH
        new_pythonpath = f"{current_pythonpath}{os.pathsep}{current_directory}" if current_pythonpath else current_directory

        # Set the new pythonpaths
        os.environ['PYTHONPATH'] = new_pythonpath
        sys.path.append(new_pythonpath)


    add_current_directory_to_pythonpath()

    from cli.__main__ import main

    main()


if __name__ == '__main__':
    init()