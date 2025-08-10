"""
user_history.py
---------------
Simple module to save and retrieve user queries.
Stores history in a local text file (history.txt).
"""

import json
from datetime import datetime

HISTORY_FILE = "history.txt"

def save_user_query(raw_input, parsed):
    """
    Saves the user's raw input and parsed data to a history file.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "raw_input": raw_input,
        "parsed": parsed
    }
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def load_user_history():
    """
    Loads all saved user queries from the history file.
    Returns a list of dictionaries.
    """
    history = []
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                history.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass  # No history file yet
    return history
