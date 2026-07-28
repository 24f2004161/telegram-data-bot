from fastapi import FastAPI, Request

from memory import add_message, get_conversation, clear_conversation
from logger import log
from llm import ask_gemini
from telegram_api import send_message

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    message = data["message"]

    chat_id = message["chat"]["id"]

    text = message["text"]

    log("received", text)

    add_message(chat_id, text)

    conversation = get_conversation(chat_id)

    answer = ask_gemini(conversation)

    log("answer", answer)

    send_message(chat_id, answer)

    clear_conversation(chat_id)

    return {"ok": True}
