"""Parse and process Tennis Abstract career data."""

import json


def _parse_matches(js_text):
    """Extract match records from career JavaScript text."""
    marker = "var morematchmx ="
    if marker not in js_text:
        raise ValueError("Career data is missing the match array.")
    array_text = js_text.split(marker, 1)[1].lstrip()
    try:
        matches, _ = json.JSONDecoder().raw_decode(array_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Career match data is not valid JSON.") from exc
    return matches