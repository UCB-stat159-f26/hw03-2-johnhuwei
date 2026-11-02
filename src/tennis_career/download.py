"""Download source text from Tennis Abstract."""

import requests


def _download_text(url):
    """Download text with a timeout and meaningful error messages."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            raise ValueError(f"Tennis Abstract data was not found: {url}") from exc
        raise ConnectionError(f"Tennis Abstract request failed: {url}") from exc
    except requests.RequestException as exc:
        raise ConnectionError(f"Could not connect to Tennis Abstract: {url}") from exc
    return response.text