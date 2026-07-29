import json

from memory import (
    add_message,
    get_conversation,
    clear_messages,
    remember_dataset,
    get_last_dataset
)

from logger import (
    log,
    start_new_log
)

from llm import ask_gemini
from config import PUBLIC_BASE_URL
from download import extract_urls, download_dataset
from executor import execute_analysis


def process_message(chat_id: int, text: str):

    # Every request starts with a fresh log
    start_new_log()

    log(
        "user_message",
        text=text
    )

    add_message(chat_id, text)

    conversation = get_conversation(chat_id)

    log(
        "conversation",
        conversation=conversation
    )

    urls = extract_urls(conversation)

    df = None

    if urls:

        url = urls[0]

        try:

            df = download_dataset(url)

            remember_dataset(
                chat_id,
                url,
                df
            )

            log(
                "dataset_loaded",
                url=url,
                rows=df.shape[0],
                columns=df.shape[1]
            )

        except Exception as e:

            log(
                "dataset_error",
                url=url,
                error=str(e)
            )

    else:

        df = get_last_dataset(chat_id)

        if df is not None:

            log(
                "dataset_reused"
            )

    if df is not None:
        try:
            answer = execute_analysis(df, conversation)

        except Exception as e:
            log("agent_error", error=str(e))
            answer = {
                "error": str(e)
            }

    else:

        llm_output = ask_gemini(conversation)

        try:
            answer = json.loads(llm_output)
        except Exception:
            answer = llm_output

    final_response = {
        "answer": answer,
        "log_url": f"{PUBLIC_BASE_URL}/run.jsonl"
    }

    log(
        "final_response",
        response=final_response
    )

    clear_messages(chat_id)

    return final_response
