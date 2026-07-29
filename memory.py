sessions = {}


def get_session(chat_id: int):

    if chat_id not in sessions:

        sessions[chat_id] = {
            "messages": [],
            "datasets": {},
            "last_dataset": None
        }

    return sessions[chat_id]


def add_message(chat_id: int, text: str):

    session = get_session(chat_id)

    session["messages"].append(text)


def get_conversation(chat_id: int):

    session = get_session(chat_id)

    return "\n".join(session["messages"])


def remember_dataset(chat_id: int, url: str, df):

    session = get_session(chat_id)

    session["datasets"][url] = df
    session["last_dataset"] = df


def get_last_dataset(chat_id: int):

    session = get_session(chat_id)

    return session["last_dataset"]


def clear_messages(chat_id: int):

    session = get_session(chat_id)

    session["messages"] = []


def clear_session(chat_id: int):

    if chat_id in sessions:
        del sessions[chat_id]
