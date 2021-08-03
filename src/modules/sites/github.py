from argparse import ArgumentDefaultsHelpFormatter
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver

class GithubDriver:
    def __init__(self, repo_settings: dict) -> None:
        self.visibility = repo_settings["visibility"]
        self.has_readme = repo_settings["readme"]
        self.has_gitignore = False
        self.profile = None
    
    def set_gitignore(self, language: str) -> None:
        """
        Sets the language for the .gitignore file, and whether to include one.

        Parameters
        ----------
        language : str
            The language that will be used for the .gitignore template file.
        """
        self.has_gitignore = True
        self.gitignore_lang = language
    
    def set_firefox_profile(self, profile_path: str) -> None:
        """
        Sets the firefox profile to be used to prevent needing credentials.

        Parameters
        ----------
        profile_path : str
            Path to the firefox profile.
        """
        self.profile = FirefoxProfile(profile_path) # Set the profile path
    
    def open_firefox(self) -> bool:
        """
        Creates a new web driver for Firefox.

        Returns
        -------
        bool
            Return True if a profile was used and the user should be
            authenticated and False if there was no profile used and therefor
            authentication should be required.
        """
        if self.profile != None:
            self.browser = webdriver.Firefox(self.profile)
            return True
        else:
            self.browser = webdriver.Firefox()
            return False
    
    def firefox_get(self, url: str) -> None:
        """
        Gets a webpage in the browser.

        Checks whether the user has opened the firefox webdriver yet. If not,
        attempts to call a function to open it and runs another function to
        login if the user is not authenticated.

        Parameters
        ----------
        url : str
            Url for the page to be retrieved.
        """
        # Check if the user has opened the browser yet
        if not self.browser:
            authenticated = self.open_firefox()
            if not authenticated:
                print("Not supported yet.")
        else:
            self.browser.get(url)
    
    def fill_creation_form(self, repo_name: str, url: str,
        repo_desc: str = "") -> None:
        self.firefox_get(url)
        repo_name_input = self.browser.find_element_by_id("repository_name")
        repo_name_input.send_keys(repo_name)

def create_github_repo(repo_settings: dict, repo_name: str, creation_url: str,
                       language: str = "", profile_path: str = "",
                       has_gitignore: bool = False) -> bool:
    """
    Creates a new repository on Github.

    Parameters
    ----------
    repo_settings : dict
        A dictionary of settings for the repository.
    repo_name : str
        The name of the repository.
    creation_url : str
        URL for the repository creation page.
    language : str
        The main programming language for the repository.
    profile_path : str
        Path to the firefox profile.
    has_gitignore : bool
        Flag for whether or not to attempt to create .gitignore file. 
    """
    # TODO: Add docstring saying that function returns whether sucessful
    driver = GithubDriver(repo_settings)
    if has_gitignore:
        driver.set_gitignore(language)
    if len(profile_path) > 0:
        driver.set_firefox_profile(profile_path)
    driver.fill_creation_form(repo_name, creation_url)
