# memory.py

conversations = {}


def add_message(chat_id: int, message: str):
    if chat_id not in conversations:
        conversations[chat_id] = []

    conversations[chat_id].append(message)


def get_conversation(chat_id: int) -> str:
    return "\n".join(conversations.get(chat_id, []))


def clear_conversation(chat_id: int):
    conversations.pop(chat_id, None)
