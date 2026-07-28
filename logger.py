import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "run.jsonl")


def start_new_log():
    """
    Create a fresh log file for every new Telegram request.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(LOG_FILE, "w") as f:
        pass


def log(event: str, **kwargs):
    """
    Append one JSON object per line.
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    }

    record.update(kwargs)

    with open(LOG_FILE, "a") as f:
        json.dump(record, f)
        f.write("\n")
