# GitHub Commit Tracker

![GitHub](https://img.shields.io/github/license/tkachenko0/GitHub-Commit-Tracker)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)

<img src="images/logo.png" alt="GitHub Commit Tracker logo" width="100"/> 

[freepik.com](https://www.freepik.com)

GitHub Commit Tracker ([@GitHubCommitTrackerBot](https://t.me/GitHubCommitTrackerBot)) is a Telegram bot that keeps you informed about the latest commits in your favorite repositories. Whether you're a developer, project manager, or tech enthusiast, this bot ensures you never miss a beat in your chosen GitHub project.

🚀 Stay in the Loop with Real-time GitHub Commits! 🚀


## Installation

1. Clone the repository:
    
```bash
git clone https://github.com/tkachenko0/GitHub-Commit-Tracker
```

2. Create a virtal environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the dependencies:

```bash
pip3 install -r requirements.txt
```

5. Configure the properties in the `.properties` file:

- `TELEGRAM_TOKEN` from the [BotFather](https://t.me/botfather)
- `GITHUB_ACCESS_TOKEN` from [GitHub](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiXqPDQmsSAAxVAS_EDHRVcB0cQFnoECA0QAQ&url=https%3A%2F%2Fgithub.com%2Fsettings%2Ftokens&usg=AOvVaw1aAJGUMBmPGH7oCTvgDvQv&opi=89978449)
- `DELAY_IN_SECONDS` is the time interval between each check expressed in seconds

At the end, the `.properties` file should look something like this:

```
ACCESS_TOKEN=ghp_GGutsdfsfssadssaxcGxc8vojZUZ3qFFwN
DELAY_IN_SECONDS=3600
TELEGRAM_TOKEN=6313830165:AAEN-z0hJV8yoIiZdwwCnEuTKwzkzkORKbho
```

## ⭐️ Usage

Run the bot:

```bash
python3 bot.py
```

Th the first step the bot will ask you the GitHub username of the user you want to track. 

Then the bot will ask you the repository name.

At the end the bot will track the commits of the user in the repository and notify ech user when a new commit is made.

## Implementation

The organization of the project is as follows:

    .
    └── db.json                      # Dataset of the chat ids and the repositories to track
    └── db.py                        # For the management of the dataset
    └── .properties.py               # For the storage of the private configuration properties
    └── configs.py                   # For the management of the private configuration properties
    └── requirments.txt              # pip dependencies
    └── tracker.py                   # For the retrieval of the commits information
    └── bot.py                       # Bot implementation

## 📜 License

This project is licensed under the [MIT License](LICENSE).

