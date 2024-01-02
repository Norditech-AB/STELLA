import os


def add_current_directory_to_pythonpath():
    # Get the directory where the script is run from
    current_directory = os.getcwd()

    # Get the current PYTHONPATH
    current_pythonpath = os.environ.get('PYTHONPATH', '')

    # Construct the new PYTHONPATH
    new_pythonpath = f"{current_pythonpath}{os.pathsep}{current_directory}" if current_pythonpath else current_directory
    # Set the new PYTHONPATH for the current session
    os.environ['PYTHONPATH'] = new_pythonpath


if not os.path.exists('app'):
    print(
        "The 'app' directory was not found. Please ensure you are running the 'serve' command from the root "
        "directory of the STELLA repository.")
    exit(1)
else:
    add_current_directory_to_pythonpath()
    from main import main
    main()
