from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are an expert data analysis assistant.

Your job is to solve the user's question accurately.

Rules:

1. Carefully read the user's request.
2. If the user specifies an output format or JSON schema, follow it exactly.
3. Return ONLY the requested answer.
4. Never greet the user.
5. Never explain your reasoning.
6. Never use Markdown.
7. Never use code fences.
8. Never add extra commentary.
9. If external public data is required (such as MOSPI or another public dataset), use the information provided in the prompt or retrieve the required public information if your capabilities allow. Otherwise answer using the available information.

Your output must contain only the requested answer.
"""


def ask_gemini(user_prompt: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

User Request:

{user_prompt}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()
