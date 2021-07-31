import os
import pwd
import subprocess as sp

def get_username() -> str:
    return pwd.getpwuid(os.getuid()).pw_name

def cd(dir_name: str):
    os.chdir(dir_name)
    print(f"Changed directory to {dir_name}")

def mkdir(dir_name: str, cd_after_creation: bool = False):
    os.mkdir(dir_name)
    print(f"Created new directory: {dir_name}")
    if cd_after_creation:
        cd(dir_name)

def run_cmd(command: str, print_result: bool = True):
    cmd = sp.Popen(command, shell=True, stdout=sp.PIPE)
    if print_result:
        print(cmd.stdout.read().decode(), end='')