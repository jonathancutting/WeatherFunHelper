import os           # detect file system type
import subprocess   # to replace deprecated os.system command

class FCOLOR:
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"

    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINKING = "\033[5m"
    STRIKETHROUGH = "\033[9m"

def clear_console():
    if os.name == "nt":     # for Windows
        subprocess.run("cls")
    else:                   # for Linux/Mac
        subprocess.run("clear")
