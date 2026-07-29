import traceback

import pandas as pd

from llm import ask_gemini
from logger import log


SYSTEM_PROMPT = """
You are an expert Python pandas programmer.

A pandas DataFrame called df already exists.

Generate ONLY executable Python code.

Rules:

1. Return ONLY Python code.
2. Do not use markdown.
3. Do not use ``` blocks.
4. Do not print anything.
5. Do not import anything.
6. Do not define functions.
7. Store the final answer in a variable named result.
8. Use only the existing DataFrame named df.
"""


def _generate_code(user_question, df, previous_error=None, previous_code=None):

    prompt = f"""
{SYSTEM_PROMPT}

Columns:
{list(df.columns)}

Data Types:
{df.dtypes.to_string()}

First 5 Rows:
{df.head().to_string(index=False)}

User Question:
{user_question}
"""

    if previous_error:

        prompt += f"""

The previous code failed.

Previous Code:

{previous_code}

Python Error:

{previous_error}

Please correct the code.
"""

    return ask_gemini(prompt).strip()


def execute_analysis(df: pd.DataFrame, user_question: str):

    previous_error = None
    previous_code = None

    for attempt in range(2):

        code = _generate_code(
            user_question,
            df,
            previous_error,
            previous_code
        )

        log(
            "generated_code",
            attempt=attempt + 1,
            code=code
        )

        local_vars = {
            "df": df,
            "pd": pd
        }

        try:

            exec(
                code,
                {
                    "__builtins__": {}
                },
                local_vars
            )

            result = local_vars.get("result")

            log(
                "execution_success",
                attempt=attempt + 1,
                result=str(result)
            )

            return result

        except Exception:

            previous_code = code
            previous_error = traceback.format_exc()

            log(
                "execution_failure",
                attempt=attempt + 1,
                error=previous_error
            )

    return {
        "error": "Unable to execute the requested analysis.",
        "details": previous_error
    }
