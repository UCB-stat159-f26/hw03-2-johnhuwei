"""Offline tests for player name handling."""

import pytest
import pandas as pd

from tennis_career.players import (_normalize_name, _parse_player_names, _resolve_player_name, _parse_player_dob)


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

@pytest.mark.parametrize(
    "page_text, expected",
    [
        ("var dob = 19810926;", "1981-09-26"),
        ("var dob=19860603;", "1986-06-03"),
    ],
)
def test_parse_player_dob(page_text, expected):
    assert _parse_player_dob(page_text) == pd.Timestamp(expected)


@pytest.mark.parametrize(
    "page_text",
    [
        "var fullname = 'Unknown Player';",
        "var dob = '';",
        "var dob = 20001301;",
        "var dob = 20000230;",
    ],
)
def test_parse_player_dob_rejects_invalid_dates(page_text):
    with pytest.raises(ValueError, match="birth date"):
        _parse_player_dob(page_text)