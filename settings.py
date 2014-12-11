# Python imports
import os

# Contrib imports
from peewee import SqliteDatabase

try:
    import local_settings
except ImportError:
    local_settings = object


def _get_config(key):
    # TODO nice error handling
    return os.environ.get(key) if os.environ.get(key) is not None else getattr(local_settings, key)

# Database location
DATABASE = 'leaderboard.db'
db = SqliteDatabase(DATABASE, threadlocals=True)

# GitHub configuration
GITHUB_USERNAME = _get_config('GITHUB_USERNAME')
GITHUB_TOKEN = _get_config('GITHUB_TOKEN')
GITHUB_REPO_OWNER = _get_config('GITHUB_REPO_OWNER')
GITHUB_REPO_NAME = _get_config('GITHUB_REPO_NAME')

# Label scores
label_scores = {
    'x-small': 1,
    'small': 2,
    'medium': 4,
    'large': 8,
    'x-large': 16,
}
