import io
import re

import pandas as pd
import requests


URL_PATTERN = re.compile(r"https?://\S+")


def extract_urls(text: str):
    """
    Extract all URLs from the user's message.
    """
    return URL_PATTERN.findall(text)


def download_dataset(url: str):
    """
    Download and load a dataset from a public URL.

    Currently supports:
    - CSV
    - JSON
    - Excel (.xlsx/.xls)

    Returns a pandas DataFrame.
    """

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    lower = url.lower()

    if lower.endswith(".csv"):
        return pd.read_csv(io.StringIO(response.text))

    if lower.endswith(".json"):
        return pd.read_json(io.StringIO(response.text))

    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        return pd.read_excel(io.BytesIO(response.content))

    raise ValueError(f"Unsupported dataset type: {url}")
