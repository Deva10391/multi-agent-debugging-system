import time
from groq import Groq, RateLimitError
from config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE, MAX_ATTEMPTS

_client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")

    last_error = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            print(f"{attempt + 1} / {MAX_ATTEMPTS}")
            response = _client.chat.completions.create(
                model=GROQ_MODEL,
                temperature=LLM_TEMPERATURE,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
            content = response.choices[0].message.content
            if not content:
                 raise RuntimeError("LLM returned empty content")
            return content.strip()
        except RateLimitError as e:
                last_error = e
                wait = 5 * (attempt + 1)
                time.sleep(wait)
    raise RuntimeError(
         f"call_llm failed after {MAX_ATTEMPTS} due to rate limit and last error was: {last_error}"
    )

"""
main-llm interaction point
"""