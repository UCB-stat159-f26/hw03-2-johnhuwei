"""Tests for career data parsing using local fixtures."""

from pathlib import Path

import pytest

from tennis_career.data import _parse_matches


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "filename, expected_opponent, expected_age",
    [
        ("FemalePlayerCareer.js", "Anne Miller", "19770119"),
        ("MalePlayerCareer.js", "Guillermo Platel", "22.264202601"),
    ],
)
def test_parse_career_fixtures(filename, expected_opponent, expected_age):
    text = (FIXTURES / filename).read_text(encoding="utf-8")
    matches = _parse_matches(text)
    assert len(matches) == 3
    assert matches[0][11] == expected_opponent
    assert matches[0][16] == expected_age


def test_parse_matches_allows_trailing_javascript():
    text = 'var morematchmx = [["example"]]; var other = 1;'
    assert _parse_matches(text) == [["example"]]


def test_parse_matches_rejects_missing_array():
    with pytest.raises(ValueError, match="missing the match array"):
        _parse_matches("var unrelated = [];")


def test_parse_matches_rejects_invalid_json():
    with pytest.raises(ValueError, match="not valid JSON"):
        _parse_matches("var morematchmx = [[")