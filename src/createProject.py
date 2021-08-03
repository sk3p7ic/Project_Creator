#!/usr/bin/env python3

"""
Creates a new project for a given language.
"""
from modules import configoperations as confops
from modules import osoperations as osops
import argparse
import sys

def get_settings(args : argparse.Namespace) -> dict:
    """
    Gets the settings based off of arguments passed and config.ini entries.

    Parameters
    ----------
    args : argparse.Namespace
        The arguments passed from argparse used to determine which settings /
        options will be used / loaded.
    
    Returns
    -------
    dict
        A dictionary of the options that were selected / used.
    """
    settings_options = {} # Holds the settings that will be used for the script
    # Check which path to use to get the configuration file for default settings
    if args.ConfigFile: # If the user specifies a configuration file path
        settings_options["config_path"] = args.ConfigFile
    else:
        config_path = "/home/sk3p7ic/.config/createProject/config.ini"
        settings_options["config_path"] = config_path
    # Set the browser to firefox (the only option available right now)
    settings_options["browser"] = confops.get_default_settings(
        settings_options["config_path"]
    )["defaultbrowser"]
    # Check if the user specified the path to a specific firefox profile
    if args.FirefoxProfile:
        settings_options["profile"] = args.FirefoxProfile
    # Check if the user specified a different website to use
    if args.UseSite:
        settings_options["website"] = args.UseSite
    else:
        settings_options["website"] = "github"
    # Check if the user specified credentials to use for a website
    if args.UseUsername and not args.UsePassword:
        print("[!] Please enter both a username and password.")
        sys.exit(1) # Exit with code 1 to show that there was an error
    elif args.UseUsername and args.UsePassword:
        site_username = args.UseUsername
        site_password = args.UsePassword
        # Add credentials to main settings
        settings_options["website_credentials"] = {
            "username": site_username,
            "password": site_password
        }
    repo_settings = {} # Stores settings for the repository being created.
    if args.RepoDescription:
        repo_settings["description"] = args.RepoDescription
    if args.RepoVisibility:
        repo_settings["visibility"] = args.RepoVisibility.lower()
    else:
        repo_settings["visibility"] = "public"
    if args.NoReadme:
        repo_settings["readme"] = False
    else:
        repo_settings["readme"] = True
    if args.ReadmeTemplate:
        if args.NoReadme:
            print("[!] Readme template supplied when README.md not requested!")
            sys.exit(1) # Exit with code 1 to show that there was an error
        else:
            repo_settings["template_file"] = args.ReadmeTemplate
    # Add the repo settings to the main settings
    settings_options["repo_settings"] = repo_settings
    # Get the parent directory for the project folder
    if args.ParentDirectory:
        settings_options["parent_dir"] = args.ParentDirectory
    else:
        project_dirs = confops.get_project_dirs(settings_options["config_path"])
        if args.ProjectLanguage:
            settings_options["parent_dir"] = project_dirs[
                args.ProjectLanguage.lower() # Get language in all lowercase
            ]
        else:
            settings_options["parent_dir"] = project_dirs[
                confops.get_default_settings(settings_options["config_path"])[
                    "defaultlanguage"
                ]
            ]
    return settings_options

def createProject(options : dict, project_name : str) -> None:
    print(options)
    project_folder_path = options["parent_dir"] + '/' + project_name
    print(project_folder_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Create a new project folder.")
    # TODO: Add arguments for program
    brwsr_grp = p.add_argument_group("Browser Options")
    brwsr_grp.add_argument(
        "-Fp", "--FirefoxProfile",
        help="Set the Firefox profile to use to log into the VCS website"
    )
    brwsr_grp.add_argument(
        "-Us", "--UseSite",
        help="The website to navigate to."
    )
    brwsr_grp.add_argument(
        "-Uu", "--UseUsername",
        help="The username to use for the website."
    )
    brwsr_grp.add_argument(
        "-Up", "--UsePassword",
        help="The password to use for the website."
    )
    repo_grp = p.add_argument_group("Repository Options")
    repo_grp.add_argument(
        "-Rd", "--RepoDescription",
        help="Description of repo to use on the VCS website."
    )
    repo_grp.add_argument(
        "-Rv", "--RepoVisibility",
        default="public",
        help="Set repo to be public/private"
    )
    repo_grp.add_argument(
        "-Nr", "--NoReadme",
        help="Don't create a README.md file for this repository.",
        action="store_true"
    )
    repo_grp.add_argument(
        "-Rt", "--ReadmeTemplate",
        help="Path to README template file to use."
    )
    p.add_argument(
        "-Cf", "--ConfigFile",
        help="The path to the configuration file to use."
    )
    p.add_argument(
        "-Pd", "--ParentDirectory",
        help="The parent directory for the project directory."
    )
    p.add_argument(
        "-Pl", "--ProjectLanguage",
        help="The main language for the project."
    )
    p.add_argument(
        "-Le", "--LoadEditor",
        help="The editor / IDE to load when the program finishes."
    )
    p.add_argument("ProjectName")
    args = p.parse_args()
    try:
        settings = get_settings(args)
        createProject(settings, args.ProjectName)
    except Exception as err:
        print("[!] A problem occurred running the program!")
        print(err)