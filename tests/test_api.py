"""Test public data retrieval without contacting live servers."""

import json
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest

from tennis_career import get_career_matches


FIXTURES = Path(__file__).parent / "fixtures"
BASE_URL = "https://www.tennisabstract.com"
DIRECTORY = 'var playerlist=["(W) Serena Williams", "(M) Rafael Nadal"];'


def _mock_sources(player_id, dob, fixture, source_path, needs_history):
    text = (FIXTURES / fixture).read_text(encoding="utf-8")
    records, _ = json.JSONDecoder().raw_decode(text.split("=", 1)[1].lstrip())
    current = records[:1] if needs_history else records
    source = (
        f"var dob={dob}; var careerjs={int(needs_history)}; "
        f"var matchmx={json.dumps(current)};"
    )
    return {
        f"{BASE_URL}/mwplayerlist.js": DIRECTORY,
        f"{BASE_URL}/{source_path}": source,
        f"{BASE_URL}/jsmatches/{player_id}Career.js": text,
    }


@pytest.mark.parametrize("needs_history", [False, True])
@pytest.mark.parametrize(
    "name, official_name, player_id, dob, fixture, source_path",
    [
        (
            "serena williams", "Serena Williams", "SerenaWilliams",
            "19810926", "FemalePlayerCareer.js",
            "jsmatches/SerenaWilliams.js",
        ),
        (
            "RafaelNadal", "Rafael Nadal", "RafaelNadal",
            "19860603", "MalePlayerCareer.js",
            "cgi-bin/player-classic.cgi?p=RafaelNadal",
        ),
    ],
)
def test_get_career_matches(
    monkeypatch, name, official_name, player_id, dob,
    fixture, source_path, needs_history,
):
    sources = _mock_sources(player_id, dob, fixture, source_path, needs_history)
    download = Mock(side_effect=sources.__getitem__)
    monkeypatch.setattr("tennis_career.api._download_text", download)
    result = get_career_matches(name)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 8)
    assert result.attrs["player_name"] == official_name
    assert result["player_age"].between(10, 50).all()
    assert result["date"].is_monotonic_increasing
    assert not result.duplicated().any()
    assert result["age_difference"].tolist() == pytest.approx(
        (result["player_age"] - result["opponent_age"]).tolist()
    )
    assert download.call_count == 2 + int(needs_history)


def test_get_career_matches_rejects_unknown_player(monkeypatch):
    download = Mock(return_value=DIRECTORY)
    monkeypatch.setattr("tennis_career.api._download_text", download)
    with pytest.raises(ValueError, match="Player not found"):
        get_career_matches("GastonSanchez")
    download.assert_called_once_with(f"{BASE_URL}/mwplayerlist.js")