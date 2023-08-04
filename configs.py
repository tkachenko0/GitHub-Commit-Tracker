from jproperties import Properties
import os

configs = Properties()
with open('.properties', 'rb') as config_file:
    configs.load(config_file)

def get(key):
    return configs.get(key).data


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DB_DIR = os.path.join(CURRENT_DIR, 'database')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

COMMIT_STATE_PATH = os.path.join(DB_DIR, 'commit_state.txt')