"""Public interface for retrieving career match data."""

from urllib.parse import quote

from .data import _add_player_age, _matches_to_frame, _parse_matches
from .download import _download_text
from .players import (
    _needs_career_file,
    _normalize_name,
    _parse_player_dob,
    _player_source_path,
    _resolve_player_name,
)


BASE_URL = "https://www.tennisabstract.com"


def _load_match_records(source, player_id):
    """Combine current and historical records when the source requires it."""
    records = _parse_matches(source, "matchmx")
    if _needs_career_file(source):
        history = _download_text(f"{BASE_URL}/jsmatches/{player_id}Career.js")
        records += _parse_matches(history)
    return records


def get_career_matches(player_name):
    """Return available career matches with ages and age differences."""
    _normalize_name(player_name)
    directory = _download_text(f"{BASE_URL}/mwplayerlist.js")
    official_name = _resolve_player_name(player_name, directory)
    player_id = quote("".join(official_name.split()), safe="")
    path = _player_source_path(official_name, directory)
    if path == "jsmatches":
        url = f"{BASE_URL}/{path}/{player_id}.js"
    else:
        url = f"{BASE_URL}/{path}?p={player_id}"
    source = _download_text(url)
    records = _load_match_records(source, player_id)
    matches = _matches_to_frame(records).drop_duplicates()
    matches = matches.sort_values("date").reset_index(drop=True)
    result = _add_player_age(matches, _parse_player_dob(source))
    result.attrs["player_name"] = official_name
    return result