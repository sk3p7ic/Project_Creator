import os
import pwd
import subprocess as sp

def get_username() -> str:
    """Get the username of the person running the program."""
    return pwd.getpwuid(os.getuid()).pw_name

def cd(dir_name: str) -> None:
    """
    Change the working directory of the program and disply a message.

    Parameters
    ----------
    dir_name : str
        The path to the directory to change to.
    """
    os.chdir(dir_name)
    print(f"Changed directory to {dir_name}")

def mkdir(dir_name: str, cd_after_creation: bool = False) -> None:
    """
    Makes new directory and displays message. Optionally changes directory.
    
    Parameters
    ----------
    dir_name : str
        The path / name of the directory to create.
    cd_after_creation : bool
        Flag to toggle whether you want to also change the current working
        directory to this directory after creation.
    """
    os.mkdir(dir_name)
    print(f"Created new directory: {dir_name}")
    if cd_after_creation:
        cd(dir_name)

def run_cmd(command: str, print_result: bool = True) -> None:
    """
    Runs a shell command.
    
    Parameters
    ----------
    command : str
        The command to attempt to run on the system.
    print_result : bool
        Flag to toggle whether to print any output from the standard output
        of the command being run.
    """
    cmd = sp.Popen(command, shell=True, stdout=sp.PIPE)
    if print_result:
        print(cmd.stdout.read().decode(), end='')