"""Resolve player names and retrieve player information."""
import json
import re
import pandas as pd

def _normalize_name(player_name):
    """Normalize spacing and case for player name comparisons."""
    if not isinstance(player_name, str):
        raise ValueError("Player name must be a non-empty string.")
    normalized = "".join(player_name.split()).casefold()
    if not normalized:
        raise ValueError("Player name must be a non-empty string.")
    return normalized

def _parse_player_names(js_text, keep_prefix=False):
    """Extract player names from the site's JavaScript list."""
    match = re.search(r"var\s+playerlist\s*=\s*", js_text)
    if match is None:
        raise ValueError("Player directory is missing the player list.")
    try:
        entries, _ = json.JSONDecoder().raw_decode(js_text[match.end():])
    except json.JSONDecodeError as exc:
        raise ValueError("Player directory contains invalid JSON.") from exc
    if keep_prefix:
        return entries
    return [re.sub(r"^\([MW]\)\s*", "", entry) for entry in entries]


def _resolve_player_name(player_name, directory_text):
    """Find a player's official name using case-insensitive matching."""
    target = _normalize_name(player_name)
    names = _parse_player_names(directory_text)
    matches = [name for name in names if _normalize_name(name) == target]
    if not matches:
        raise ValueError(f"Player not found: {player_name!r}. Check the spelling.")
    if len(matches) > 1:
        raise ValueError(f"Player name is ambiguous: {player_name!r}.")
    return matches[0]

def _parse_player_dob(page_text):
    """Extract and validate a player's birth date from page source."""
    match = re.search(r"\bvar\s+dob\s*=\s*(\d{8})\s*;", page_text)
    if match is None:
        raise ValueError("Player page is missing a valid birth date.")
    try:
        return pd.to_datetime(match.group(1), format="%Y%m%d", errors="raise")
    except ValueError as exc:
        raise ValueError("Player page contains an invalid birth date.") from exc

def _player_source_path(official_name, directory_text):
    """Choose the match-data source using the directory's tour marker."""
    entries = _parse_player_names(directory_text, keep_prefix=True)
    if f"(W) {official_name}" in entries:
        return "jsmatches"
    if f"(M) {official_name}" in entries:
        return "cgi-bin/player-classic.cgi"
    raise ValueError("Player is missing a recognized tour marker.")


def _needs_career_file(source_text):
    """Read whether the source requires an additional career file."""
    match = re.search(r"\bvar\s+careerjs\s*=\s*([01])\s*;", source_text)
    if match is None:
        raise ValueError("Player source is missing the career-data flag.")
    return match.group(1) == "1"