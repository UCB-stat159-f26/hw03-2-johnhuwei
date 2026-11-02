"""Resolve player names and retrieve player information."""
import json
import re

def _normalize_name(player_name):
    """Normalize spacing and case for player name comparisons."""
    if not isinstance(player_name, str):
        raise ValueError("Player name must be a non-empty string.")
    normalized = "".join(player_name.split()).casefold()
    if not normalized:
        raise ValueError("Player name must be a non-empty string.")
    return normalized

def _parse_player_names(js_text):
    """Extract player names from the site's JavaScript list."""
    match = re.search(r"var\s+playerlist\s*=\s*", js_text)
    if match is None:
        raise ValueError("Player directory is missing the player list.")
    try:
        entries, _ = json.JSONDecoder().raw_decode(js_text[match.end():])
    except json.JSONDecodeError as exc:
        raise ValueError("Player directory contains invalid JSON.") from exc
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