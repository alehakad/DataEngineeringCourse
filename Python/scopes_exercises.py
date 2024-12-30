import os
import platform
import sys

def check_name_in_globals(given_name: str):
    return given_name in globals()

def print_os_vars():
    # print os name
    print(os.name, platform.system())
    # name of logged in user
    print(os.getlogin())
    # current working directory
    print(os.getcwd())

def print_cmdargs_reversed():
    print(sys.argv[::-1])

def check_executable_file(file_name: str):
    file_name = sys.argv[1]
    # search for file in current directory
    if not os.path.exists(file_name):
        print(f"File {file_name} not found")
        return
    # check if file is executable
    if not os.access(file_name, os.X_OK):
        print(f"File {file_name} is not executable")
        # change it for owner and group
        os.chmod(file_name, 0o755)
        return
    print(f"File {file_name} is executable")     


if __name__ == "__main__":
    assert not check_name_in_globals("remove_words")
    assert check_name_in_globals("__name__")


    print_os_vars()
    print("All tests passed.")

    print_cmdargs_reversed()

    check_executable_file(sys.argv[1])

