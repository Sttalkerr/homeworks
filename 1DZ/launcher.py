import subprocess
import os

def launch_shell():
    subprocess.Popen(['python', 'shell.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    launch_shell()
