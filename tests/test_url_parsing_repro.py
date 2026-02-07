from urllib.parse import urlparse

def parse_github_url(url: str):
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    
    if len(path_parts) >= 4 and path_parts[2] == "tree":
        # Format: /user/repo/tree/branch/subdir...
        user = path_parts[0]
        repo = path_parts[1]
        branch = path_parts[3]
        subdir = "/".join(path_parts[4:])
        repo_url = f"{parsed.scheme}://{parsed.netloc}/{user}/{repo}.git"
        return repo_url, branch, subdir
    else:
        # Format: /user/repo or /user/repo.git
        if url.endswith(".git"):
            repo_url = url
        else:
            repo_url = f"{url}.git"
        return repo_url, None, None

def test_parsing():
    # Test case 1: Subdirectory with branch
    url1 = "https://github.com/ComposioHQ/awesome-claude-skills/tree/master/activecampaign-automation"
    repo, branch, subdir = parse_github_url(url1)
    print(f"URL: {url1}")
    print(f"Repo: {repo}, Branch: {branch}, Subdir: {subdir}")
    assert repo == "https://github.com/ComposioHQ/awesome-claude-skills.git"
    assert branch == "master"
    assert subdir == "activecampaign-automation"

    # Test case 2: Standard repo
    url2 = "https://github.com/user/repo"
    repo, branch, subdir = parse_github_url(url2)
    print(f"\nURL: {url2}")
    print(f"Repo: {repo}, Branch: {branch}, Subdir: {subdir}")
    assert repo == "https://github.com/user/repo.git"
    assert branch is None
    assert subdir is None

if __name__ == "__main__":
    test_parsing()
