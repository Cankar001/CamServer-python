from colorama import Fore
from colorama import Style

LOGGER_ENABLED = True
DEBUGGING_ENABLED = False

def enableDebugger():
    global DEBUGGING_ENABLED
    DEBUGGING_ENABLED = True


def enableLogger():
    global LOGGER_ENABLED
    LOGGER_ENABLED = True


def disableLogger():
    global LOGGER_ENABLED
    LOGGER_ENABLED = False


def debug(msg):
    global LOGGER_ENABLED
    global DEBUGGING_ENABLED

    if not LOGGER_ENABLED:
        return

    if DEBUGGING_ENABLED:
        print(f"{Style.BRIGHT}{Fore.CYAN}" + str(msg) + f"{Style.RESET_ALL}")

def trace(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.WHITE}" + str(msg) + f"{Style.RESET_ALL}")

def error(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.RED}" + '[ERROR]: ' + str(msg) + f"{Style.RESET_ALL}")

def critical(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.RED}" + '[CRITICAL ERROR]: ' + str(msg) + f"{Style.RESET_ALL}")

def info(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.BLUE}" + str(msg) + f"{Style.RESET_ALL}")

def warn(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.YELLOW}" + '[WARNING]: ' + str(msg) + f"{Style.RESET_ALL}")

def success(msg):
    global LOGGER_ENABLED

    if not LOGGER_ENABLED:
        return

    print(f"{Style.BRIGHT}{Fore.GREEN}" + str(msg) + f"{Style.RESET_ALL}")

