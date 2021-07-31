from . import osoperations
import configparser

def read_config_file(config_file: str = "", username: str = ""):
    config = configparser.ConfigParser()
    # If the config file was not specified, set the path to user's config files
    if config_file == "":
        config_file = f"/home/{username}/.config/project-creator/config.ini"
    try:
        config.read(config_file)
    except configparser.Error as err:
        print(err)
    except FileNotFoundError as err:
        print(f"[!] File not found!\n{err}")
    return config

def get_default_settings(config_file: str = "", username: str = ""):
    if username == "":
        username = osoperations.get_username()
    config = read_config_file(config_file, username)
    default_settings = {}
    for key in config["Default"]:
        default_settings[key] = config["Default"][key]
    return default_settings

def get_project_dirs(config_file: str = "", username: str = ""):
    if username == "":
        username = osoperations.get_username()
    config = read_config_file(config_file, username)
    project_dirs = {}
    for key in config["ProjectDirectories"]:
        project_dirs[key] = config["ProjectDirectories"][key].replace(
            "~/", f"/home/{username}/"
        )
        project_dirs[key].replace("~/", f"/home/{username}")
    return project_dirs