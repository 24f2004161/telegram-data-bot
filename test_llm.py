from llm import ask_gemini

print(
    ask_gemini(
        """
Return ONLY this JSON:

{
    "state":"Tamil Nadu"
}
"""
    )
)
