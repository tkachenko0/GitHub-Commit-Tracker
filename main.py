from github import Github, Auth
import configs
import time

# Attention: this token may be already expired
ACCESS_TOKEN = configs.get("ACCESS_TOKEN")
REPO_OWNER = configs.get("REPO_OWNER")
REPO_NAME = configs.get("REPO_NAME")
COMMIT_STATE_PATH = configs.COMMIT_STATE_PATH
DELAY = int(configs.get("DELAY_IN_SECONDS"))


def save_commit_state(commit_sha: str):
    """Saves the commit state to a file or database."""
    with open(COMMIT_STATE_PATH, 'w') as state_file:
        state_file.write(commit_sha)


def load_commit_state():
    """Loads the commit state from a file or database."""
    try:
        with open(COMMIT_STATE_PATH, 'r') as state_file:
            return state_file.read().strip()
    except FileNotFoundError:
        return None


def main():
    auth = Auth.Token(ACCESS_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(f'{REPO_OWNER}/{REPO_NAME}')

    while True:
        saved_commit_state = load_commit_state()

        commits = repo.get_commits()

        for commit in commits:
            commit_sha = commit.sha
            if commit_sha == saved_commit_state:
                break  # We've reached the last saved commit, no need to process further

            date = commit.commit.author.date
            message = commit.commit.message

            print(f'Date: {date}')
            print(f'Message: {message}')

        # Save the latest commit state
        latest_commit = commits[0].sha if commits else None
        if latest_commit:
            save_commit_state(latest_commit)

        # Wait for a specified interval before checking again
        time.sleep(DELAY)


if __name__ == '__main__':
    main()
