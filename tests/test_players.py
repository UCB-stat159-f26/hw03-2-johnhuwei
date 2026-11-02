"""Offline tests for player name handling."""

import pytest

from tennis_career.players import _normalize_name


@pytest.mark.parametrize(
    "player_name",
    [
        "serena williams",
        "Serena Williams",
        "SerenaWilliams",
        "  Serena\tWilliams  ",
    ],
)
def test_normalize_name_accepts_name_variations(player_name):
    assert _normalize_name(player_name) == "serenawilliams"


@pytest.mark.parametrize("player_name", ["", "   ", None, 123])
def test_normalize_name_rejects_invalid_input(player_name):
    with pytest.raises(ValueError, match="non-empty string"):
        _normalize_name(player_name)