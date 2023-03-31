import os


def OPENAI_API_KEY() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key
