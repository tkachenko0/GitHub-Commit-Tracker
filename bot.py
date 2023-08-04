from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import Update, ParseMode
import configs
import tracker
import db

TELEGRAM_TOKEN = configs.get_property('TELEGRAM_TOKEN')
DELAY_IN_SECONDS = int(configs.get_property('DELAY_IN_SECONDS'))
DB_PATH = db.DB_PATH

REPO_OWNER, REPO_NAME = range(2)

already_started = False

def send_message(context, chat_id, message) -> None:
    context.bot.send_message(
                chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)

def build_message(commit) -> str:
    date = commit.commit.author.date
    message = commit.commit.message
    modified_files = [file.filename for file in commit.files]
    mess_to_send = f'<b>New commit</b> at {date.hour}:{date.minute} on {date.day}/{date.month}/{date.year}.\n'
    mess_to_send += f'<b>Message</b>: {message}\n'
    
    if modified_files:
        mess_to_send += '<b>Modified files</b>:\n'
        for file in modified_files:
            mess_to_send += f'• {file}\n'
    else:
        mess_to_send += '*<b>No modified files</b>.\n'

    return mess_to_send


def check_commits(context) -> None:
    rows = db.get_all_entries()
    
    for row in rows:
        chat_id = row['chat_id']
        repo_owner = row['repo_owner']
        repo_name = row['repo_name']
        last_commit_sha = row['last_commit_sha']

        repo = tracker.get_repo(repo_owner, repo_name)
        commits = tracker.get_not_reported_commits(repo, last_commit_sha)

        for commit in commits:
            send_message(context, chat_id, build_message(commit))

        # Save the latest commit state
        latest_commit = commits[0].sha if commits else None
        if latest_commit:
            db.save_commit_state(chat_id, latest_commit)


def start(update, context) -> int:
    chat_id = update.message.chat_id
    send_message(context, chat_id, 'Welcome to the <b>Commit Tracker Bot</b>. Please insert the <b>repo owner</b>.')

    return REPO_OWNER


def repo_owner(update, context) -> int:
    chat_id = update.message.chat_id
    repo_owner = update.message.text.strip()

    new_entry = {
        'chat_id': chat_id,
        'repo_owner': repo_owner,
        'repo_name': '',
        'last_commit_sha': ''
    }

    db.init_entry(new_entry)

    send_message(context, chat_id, 'Now please insert the <b>repo name</b>.')
    
    return REPO_NAME


def repo_name(update, context) -> None:
    global already_started

    chat_id = update.message.chat_id
    repo_name = update.message.text.strip()
    repo_owner = db.get_property(chat_id, "repo_owner")

    try:
        last_commit_sha = tracker.get_last_commit_sha(repo_owner, repo_name)
    except:
        send_message(context, chat_id, 'Error: repo not found. retry with /start')
        return ConversationHandler.END

    db.update_propery(chat_id, "repo_name", repo_name)
    db.update_propery(chat_id, "last_commit_sha", last_commit_sha)

    if not already_started:
        already_started = True
        context.job_queue.run_repeating(
            check_commits, DELAY_IN_SECONDS, context=chat_id)

    send_message(context, chat_id, f'You are now subscribed to the repo <b>{repo_name}</b> of <b>{repo_owner}</b>.')
    send_message(context, chat_id, 'You will receive a message every time a new commit is pushed to the repo.')
    
    return REPO_NAME


def unscribe(update, context) -> None:
    chat_id = update.message.chat_id
    db.remove_entry(chat_id)
    context.bot.send_message(chat_id=chat_id, text='Unsubscribed')


def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REPO_OWNER: [MessageHandler(Filters.text & ~Filters.command, repo_owner)],
            REPO_NAME: [MessageHandler(Filters.text & ~Filters.command, repo_name)],
        },
        fallbacks=[CommandHandler('unscribe', unscribe)]
    )
    
    dp.add_handler(conv_handler)
    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


main()
