from github import Github, Auth
import configs
import configs

ACCESS_TOKEN = configs.get_property("ACCESS_TOKEN")
REPO_OWNER = "anticorruzione"
REPO_NAME = "npa"
DELAY = configs.get_property("DELAY_IN_SECONDS")


def get_repo(repo_owner: str, repo_name: str):
    auth = Auth.Token(ACCESS_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')
    return repo


def get_last_commit_sha(repo_owner: str, repo_name: str) -> str:
    """Gets the last commit sha from a file or database."""
    repo = get_repo(repo_owner, repo_name)
    commits = repo.get_commits()
    return commits[0].sha if commits else None


def get_not_reported_commits(repo: str, last_commit_sha: str) -> list:
    """Gets the commuts that haven't been reposted yet."""
    commits = repo.get_commits()
    not_reported = []
    if last_commit_sha:
        for commit in commits:
            if commit.sha == last_commit_sha:
                break
            not_reported.append(commit)
    return not_reported
