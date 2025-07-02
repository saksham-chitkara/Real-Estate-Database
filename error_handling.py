from colorama import Fore, Style, init
init(autoreset=True)

def incomplete_arguments(cmd_name: str):
    print(f"{cmd_name} : Incomplete Arguments")


def invalid_arguments(cmd_name: str, attr_name: str, options: list):
    print(f"{cmd_name}:{attr_name} : Invalid Argument > {options}")


def compare_list(length: int, ideal: int, cmd_name: str):
    if length < ideal:
        incomplete_arguments(cmd_name)
        return True
    return False


def db_error(err_msg: str):
    print(Fore.RED + f"Database Error: {err_msg}")


def permission_error(cmd_name: str):
    print(f"{cmd_name} : Permission Denied")
