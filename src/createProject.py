"""
Creates a new project for a given language.
"""
from modules import configoperations as confops
from modules import osoperations as osops

def main():
    print(confops.get_default_settings("src/config.ini"))
    print(confops.get_project_dirs("src/config.ini"))
    osops.run_cmd("echo 'Hello world!'")

if __name__ == "__main__":
    main()