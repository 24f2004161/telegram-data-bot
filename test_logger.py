from logger import *

start_new_log()

log(
    "user_message",
    text="Hello"
)

log(
    "conversation",
    conversation="Hello"
)

log(
    "llm_response",
    response='{"answer":"Hello"}'
)

log(
    "telegram_reply",
    response='{"answer":"Hello"}'
)

print("Logger working successfully.")
