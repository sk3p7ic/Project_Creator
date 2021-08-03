
def create_repo_with_site(site_name: str, settings: dict) -> None:
    if site_name.lower() == "github":
        from modules.sites import github
        # Code here
