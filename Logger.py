from colorama import Fore
from colorama import Style

def debug(msg):
    print(f"{Style.BRIGHT}{Fore.CYAN}" + str(msg) + f"{Style.RESET_ALL}")

def trace(msg):
    print(f"{Style.BRIGHT}{Fore.WHITE}" + str(msg) + f"{Style.RESET_ALL}")

def error(msg):
    print(f"{Style.BRIGHT}{Fore.RED}" + '[ERROR]: ' + str(msg) + f"{Style.RESET_ALL}")

def critical(msg):
    print(f"{Style.BRIGHT}{Fore.RED}" + '[CRITICAL ERROR]: ' + str(msg) + f"{Style.RESET_ALL}")

def info(msg):
    print(f"{Style.BRIGHT}{Fore.BLUE}" + str(msg) + f"{Style.RESET_ALL}")

def warn(msg):
    print(f"{Style.BRIGHT}{Fore.YELLOW}" + '[WARNING]: ' + str(msg) + f"{Style.RESET_ALL}")

def success(msg):
    print(f"{Style.BRIGHT}{Fore.GREEN}" + str(msg) + f"{Style.RESET_ALL}")

