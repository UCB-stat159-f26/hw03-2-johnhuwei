"""Offline tests for player name handling."""

import pytest

from tennis_career.players import (_normalize_name, _parse_player_names, _resolve_player_name)


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

DIRECTORY = (
    'var playerlist=["(W) Serena Williams", "(M) Rafael Nadal"];'
)


def test_parse_player_names():
    assert _parse_player_names(DIRECTORY) == ["Serena Williams", "Rafael Nadal"]


@pytest.mark.parametrize(
    "name, expected",
    [
        ("serena williams", "Serena Williams"),
        ("SerenaWilliams", "Serena Williams"),
        ("rafael nadal", "Rafael Nadal"),
    ],
)
def test_resolve_player_name(name, expected):
    assert _resolve_player_name(name, DIRECTORY) == expected


def test_resolve_player_name_rejects_unknown_player():
    with pytest.raises(ValueError, match="Player not found"):
        _resolve_player_name("GastonSanchez", DIRECTORY)


@pytest.mark.parametrize("text", ["var other = [];", "var playerlist = ["])
def test_parse_player_names_rejects_invalid_directory(text):
    with pytest.raises(ValueError, match="Player directory"):
        _parse_player_names(text)


def test_resolve_player_name_rejects_ambiguous_names():
    directory = 'var playerlist=["(M) Alex Smith", "(W) Alex Smith"];'
    with pytest.raises(ValueError, match="ambiguous"):
        _resolve_player_name("Alex Smith", directory)