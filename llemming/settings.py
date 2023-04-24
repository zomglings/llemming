import os
from typing import List

import openai


def OPENAI_API_KEY() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key


def max_tokens(model_id: str) -> int:
    """
    There currently is no programmatic way of obtaining this information via the OpenAI API.

    I have pulled this information from their documentation: https://platform.openai.com/docs/models
    """
    if model_id.startswith("gpt-4"):
        if "32k" in model_id:
            return 32768
        else:
            return 8192
    elif model_id.startswith("gpt-3.5"):
        return 4096
    elif model_id == "text-davinci-003" or model_id == "text-davinci-002":
        return 4097
    elif model_id == "code-davinci-002":
        return 8001
    else:
        return 2049


def MODELS(refetch: bool = False) -> List[str]:
    """
    Cached model list was produced as follows:
    >>> models_response = openai.Model.list()
    >>> models = [model["id"] for model in models_response.data]

    The cached models list was last calculated at: Sun 23 Apr 2023 11:44:52 PM UTC
    """

    models: List[str] = [
        "babbage",
        "davinci",
        "text-davinci-edit-001",
        "gpt-3.5-turbo-0301",
        "babbage-code-search-code",
        "text-similarity-babbage-001",
        "gpt-3.5-turbo",
        "code-davinci-edit-001",
        "text-davinci-001",
        "text-davinci-003",
        "ada",
        "babbage-code-search-text",
        "babbage-similarity",
        "gpt-4",
        "code-search-babbage-text-001",
        "text-curie-001",
        "whisper-1",
        "gpt-4-0314",
        "code-search-babbage-code-001",
        "text-ada-001",
        "text-embedding-ada-002",
        "text-similarity-ada-001",
        "curie-instruct-beta",
        "ada-code-search-code",
        "ada-similarity",
        "code-search-ada-text-001",
        "text-search-ada-query-001",
        "davinci-search-document",
        "ada-code-search-text",
        "text-search-ada-doc-001",
        "davinci-instruct-beta",
        "text-similarity-curie-001",
        "code-search-ada-code-001",
        "ada-search-query",
        "text-search-davinci-query-001",
        "curie-search-query",
        "davinci-search-query",
        "babbage-search-document",
        "ada-search-document",
        "text-search-curie-query-001",
        "text-search-babbage-doc-001",
        "curie-search-document",
        "text-search-curie-doc-001",
        "babbage-search-query",
        "text-babbage-001",
        "text-search-davinci-doc-001",
        "text-search-babbage-query-001",
        "curie-similarity",
        "curie",
        "text-similarity-davinci-001",
        "text-davinci-002",
        "davinci-similarity",
        "cushman:2020-05-03",
        "ada:2020-05-03",
        "babbage:2020-05-03",
        "curie:2020-05-03",
        "davinci:2020-05-03",
        "if-davinci-v2",
        "if-curie-v2",
        "if-davinci:3.0.0",
        "davinci-if:3.0.0",
        "davinci-instruct-beta:2.0.0",
        "text-ada:001",
        "text-davinci:001",
        "text-curie:001",
        "text-babbage:001",
    ]

    if refetch:
        openai.api_key = OPENAI_API_KEY()
        models_response = openai.Model.list()
        models = [model["id"] for model in models_response.data]

    return models
