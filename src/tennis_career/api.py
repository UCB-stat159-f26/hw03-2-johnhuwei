"""Public interface for retrieving career match data."""

from urllib.parse import quote

from .data import _add_player_age, _matches_to_frame, _parse_matches
from .download import _download_text
from .players import _normalize_name, _parse_player_dob, _resolve_player_name


BASE_URL = "https://www.tennisabstract.com"


def get_career_matches(player_name):
    """Return career matches with player ages and opponent age differences."""
    _normalize_name(player_name)
    directory = _download_text(f"{BASE_URL}/mwplayerlist.js")
    official_name = _resolve_player_name(player_name, directory)
    player_id = quote("".join(official_name.split()), safe="")
    profile = _download_text(f"{BASE_URL}/cgi-bin/player.cgi?p={player_id}")
    birth_date = _parse_player_dob(profile)
    career = _download_text(f"{BASE_URL}/jsmatches/{player_id}Career.js")
    matches = _matches_to_frame(_parse_matches(career))
    result = _add_player_age(matches, birth_date)
    result.attrs["player_name"] = official_name
    return result