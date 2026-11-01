"""Parse and process Tennis Abstract career data."""

import json
import pandas as pd

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

def _opponent_age(age_value, match_date):
    """Convert an opponent birth date or numeric age to years."""
    text = str(age_value).strip()
    if len(text) == 8 and text.isdigit():
        birth_date = pd.to_datetime(text, format="%Y%m%d", errors="raise")
        age = (pd.Timestamp(match_date) - birth_date).days / 365.25
    else:
        age = float(text)
    if not 0 <= age < 120:
        raise ValueError("Opponent age must be between 0 and 120 years.")
    return age