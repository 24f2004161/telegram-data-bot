import json
import os
from datetime import datetime

LOG_FILE = "logs/run.jsonl"


def log(step: str, content):
    os.makedirs("logs", exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "step": step,
        "content": content
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
