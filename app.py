from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import os

from memory import (
    add_message,
    get_conversation,
    clear_conversation
)

from logger import (
    start_new_log,
    log,
    LOG_FILE
)

from llm import ask_gemini
from telegram_api import send_message

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "running"
    }


@app.get("/run.jsonl")
def get_log():

    if not os.path.exists(LOG_FILE):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Log file not found"
            }
        )

    return FileResponse(
        LOG_FILE,
        media_type="application/json"
    )


@app.post("/webhook")
async def webhook(request: Request):

    start_new_log()

    data = await request.json()

    if "message" not in data:
        return {"ok": True}

    message = data["message"]

    if "text" not in message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message["text"]

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

    answer = ask_gemini(conversation)

    log(
        "llm_prompt",
        prompt=conversation
    )

    log(
        "llm_response",
        response=answer
    )

    send_message(chat_id, answer)

    log(
        "telegram_reply",
        response=answer
    )

    clear_conversation(chat_id)

    return {
        "ok": True
    }
