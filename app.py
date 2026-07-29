from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import json
import os

from logger import (
    start_new_log,
    log,
    LOG_FILE
)

from telegram_api import send_message
from agent import process_message

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

    data = await request.json()

    if "message" not in data:
        return {"ok": True}

    message = data["message"]

    if "text" not in message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message["text"]

    final_response = process_message(
        chat_id,
        text
    )

    send_message(
        chat_id,
        json.dumps(
            final_response,
            ensure_ascii=False
        )
    )

    log(
        "telegram_reply",
        response=final_response
    )

    return {
        "ok": True
    }
