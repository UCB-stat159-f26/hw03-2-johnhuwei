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

def _matches_to_frame(matches):
    """Build a clean match table from parsed career records."""
    fields = {
        "date": 0,
        "tournament": 1,
        "surface": 2,
        "result": 4,
        "opponent": 11,
        "opponent_age": 16,
    }
    rows = [{name: row[index] for name, index in fields.items()} for row in matches]
    frame = pd.DataFrame(rows, columns=list(fields))
    frame["date"] = pd.to_datetime(frame["date"], format="%Y%m%d", errors="raise")
    frame["opponent_age"] = [
        _opponent_age(value, date)
        for value, date in zip(frame["opponent_age"], frame["date"])
    ]
    return frame

def _add_player_age(matches, player_dob):
    """Add player age and age difference without changing the input."""
    frame = matches.copy()
    birth_date = pd.Timestamp(player_dob)
    if pd.isna(birth_date) or (frame["date"] < birth_date).any():
        raise ValueError("Player birth date must be valid and not after matches.")
    frame["player_age"] = (frame["date"] - birth_date).dt.days / 365.25
    frame["age_difference"] = frame["player_age"] - frame["opponent_age"]
    return frame