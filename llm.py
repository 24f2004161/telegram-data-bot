import time

from google import genai
from google.genai import errors

from config import GEMINI_API_KEY
from logger import log

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are an expert data analysis assistant.

Rules:
1. Return only the requested answer.
2. Do not use markdown.
3. Do not explain your reasoning.
4. Follow any requested JSON schema exactly.
"""


def ask_gemini(user_prompt: str, retries: int = 3) -> str:
    """
    Send a prompt to Gemini with automatic retry and logging.
    """

    prompt = f"""
{SYSTEM_PROMPT}

User Request:

{user_prompt}
"""

    log("llm_prompt", prompt=prompt)

    last_error = None

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            log(
                "llm_response",
                attempt=attempt + 1,
                response=text
            )

            return text

        except Exception as e:

            last_error = str(e)

            log(
                "llm_error",
                attempt=attempt + 1,
                error=last_error
            )

            # Exponential backoff
            time.sleep(2 ** attempt)

    # Return a structured error instead of raising
    return """
{
    "error": "Gemini API is temporarily unavailable. Please try again later."
}
"""
