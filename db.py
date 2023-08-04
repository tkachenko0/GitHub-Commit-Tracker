import json
import os


def set_db():
    """Sets the database."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(current_dir, 'db.json')
    if not os.path.exists(db_path):
        with open(db_path, "w") as file:
            json.dump([], file)
    return db_path


DB_PATH = set_db()

def get_all_entries() -> list:
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        return db
    

def init_entry(new_entry: dict):
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        if db != None and len(db) > 0:
            for entry in db:
                if entry["chat_id"] == new_entry["chat_id"]:
                    entry["repo_owner"] = new_entry["repo_owner"]
                    entry["repo_name"] = new_entry["repo_name"]
                    entry["last_commit_sha"] = new_entry["last_commit_sha"]
                    break
        else:
            db.append(new_entry)
    with open(DB_PATH, "w") as file:
        json.dump(db, file)


def remove_entry(chat_id: str):
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        for entry in db:
            if entry["chat_id"] == chat_id:
                db.remove(entry)
                break
    with open(DB_PATH, "w") as file:
        json.dump(db, file)


def update_propery(chat_id: str, property: str, value: str):
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        for entry in db:
            if entry["chat_id"] == chat_id:
                entry[property] = value
    with open(DB_PATH, "w") as file:
        json.dump(db, file)

def get_property(chat_id: str, property: str) -> str:
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        for entry in db:
            if entry["chat_id"] == chat_id:
                return entry[property]
    return None


def save_commit_state(chat_id: str, last_commit_sha: str):
    with open(DB_PATH, "r") as file:
        db = json.load(file)
        for entry in db:
            if entry["chat_id"] == chat_id:
                entry["last_commit_sha"] = last_commit_sha
    with open(DB_PATH, "w") as file:
        json.dump(db, file)
