import os


def add_current_directory_to_pythonpath():
    # Get the directory where the script is run from
    current_directory = os.getcwd()

    # Get the current PYTHONPATH
    current_pythonpath = os.environ.get('PYTHONPATH', '')

    print(current_pythonpath)

    # Construct the new PYTHONPATH
    new_pythonpath = f"{current_pythonpath}{os.pathsep}{current_directory}" if current_pythonpath else current_directory
    # Set the new PYTHONPATH for the current session
    os.environ['PYTHONPATH'] = new_pythonpath
    print(new_pythonpath)



#add_current_directory_to_pythonpath()
from stella.main import main
main()
