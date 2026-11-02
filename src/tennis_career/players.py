"""Resolve player names and retrieve player information."""


def _normalize_name(player_name):
    """Normalize spacing and case for player name comparisons."""
    if not isinstance(player_name, str):
        raise ValueError("Player name must be a non-empty string.")
    normalized = "".join(player_name.split()).casefold()
    if not normalized:
        raise ValueError("Player name must be a non-empty string.")
    return normalized