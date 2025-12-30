# Imports
import json
from pathlib import Path

# Path to JSON file
DB_FILE = Path(__file__).resolve().parent / "users.json"

# Variables
START_CREDITS = 5

# Functions
def load_users():
    if not DB_FILE.exists():
        return {}
    return json.loads(DB_FILE.read_text())

def save_users(users):
    DB_FILE.write_text(json.dumps(users, indent=2))