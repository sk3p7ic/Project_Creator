"""
Creates a new project for a given language.
"""
from modules import configoperations as confops
from modules import osoperations as osops
import argparse
import sys

def main(args : argparse.Namespace):
    # Check if user specified a specific configuration file to use.
    settings_options = {}
    if args.ConfigFile:
        settings_options["config_path"] = args.ConfigFile
    else:
        settings_options["config_path"] = "src/config.ini" # TODO: Change to ~/.config/createProject
    if args.FirefoxProfile:
        settings_options["profile"] = args.FirefoxProfile
    if args.UseSite:
        settings_options["website"] = args.UseSite
    if args.UseUsername and not args.UsePassword:
        print("[!] Please enter both a username and password.")
        sys.exit(1) # Exit with code 1 to show that there was an error
    elif args.UseUsername and args.UsePassword:
        site_username = args.UseUsername
        site_password = args.UsePassword
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
    settings_options["repo_settings"] = repo_settings
    if args.ParentDirectory:
        settings_options["parent_dir"] = args.ParentDirectory
    else:
        project_dirs = confops.get_project_dirs(settings_options["config_path"])
        if args.ProjectLanguage:
            settings_options["parent_dir"] = project_dirs[args.ProjectLanguage]
        else:
            settings_options["parent_dir"] = project_dirs[
                confops.get_default_settings(settings_options["config_path"])[
                    "defaultlanguage"
                ]
            ]
    print(settings_options)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Create a new project folder.")
    # TODO: Add arguments for program
    brwsr_grp = p.add_argument_group("Browser Options")
    brwsr_grp.add_argument(
        "-Fp", "--FirefoxProfile",
        help="Set the Firefox profile to use to log into the VCS website",
        action="store_true"
    )
    brwsr_grp.add_argument(
        "-Us", "--UseSite",
        help="The website to navigate to.",
        action="store_true"
    )
    brwsr_grp.add_argument(
        "-Uu", "--UseUsername",
        help="The username to use for the website.",
        action="store_true"
    )
    brwsr_grp.add_argument(
        "-Up", "--UsePassword",
        help="The password to use for the website.",
        action="store_true"
    )
    repo_grp = p.add_argument_group("Repository Options")
    repo_grp.add_argument(
        "-Rd", "--RepoDescription",
        help="Description of repo to use on the VCS website.",
        action="store_true"
    )
    repo_grp.add_argument(
        "-Rv", "--RepoVisibility",
        default="public",
        help="Set repo to be public/private",
        action="store_true"
    )
    repo_grp.add_argument(
        "-Nr", "--NoReadme",
        help="Don't create a README.md file for this repository.",
        action="store_true"
    )
    repo_grp.add_argument(
        "-Rt", "--ReadmeTemplate",
        help="Path to README template file to use.",
        action="store_true"
    )
    p.add_argument(
        "-Cf", "--ConfigFile",
        default="src/config.ini",
        help="The path to the configuration file to use.",
        action="store_true"
    )
    p.add_argument(
        "-Pd", "--ParentDirectory",
        help="The parent directory for the project directory.",
        action="store_true"
    )
    p.add_argument(
        "-Pl", "--ProjectLanguage",
        help="The main language for the project.",
        action="store_true"
    )
    p.add_argument(
        "-Le", "--LoadEditor",
        help="The editor / IDE to load when the program finishes.",
        action="store_true"
    )
    args = p.parse_args()
    main(args)