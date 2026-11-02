"""Test the public data function using simulated downloads."""

from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest

from tennis_career import get_career_matches


FIXTURES = Path(__file__).parent / "fixtures"
BASE_URL = "https://www.tennisabstract.com"
DIRECTORY = 'var playerlist=["(W) Serena Williams", "(M) Rafael Nadal"];'


@pytest.mark.parametrize(
    "name, official_name, player_id, dob, fixture",
    [
        (
            "serena williams", "Serena Williams", "SerenaWilliams",
            "19810926", "FemalePlayerCareer.js",
        ),
        (
            "RafaelNadal", "Rafael Nadal", "RafaelNadal",
            "19860603", "MalePlayerCareer.js",
        ),
    ],
)
def test_get_career_matches(monkeypatch, name, official_name, player_id, dob, fixture):
    sources = {
        f"{BASE_URL}/mwplayerlist.js": DIRECTORY,
        f"{BASE_URL}/cgi-bin/player.cgi?p={player_id}": f"var dob = {dob};",
        f"{BASE_URL}/jsmatches/{player_id}Career.js":
            (FIXTURES / fixture).read_text(encoding="utf-8"),
    }
    download = Mock(side_effect=sources.__getitem__)
    monkeypatch.setattr("tennis_career.api._download_text", download)
    result = get_career_matches(name)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 8)
    assert result.attrs["player_name"] == official_name
    assert result["player_age"].between(10, 50).all()
    assert result["age_difference"].tolist() == pytest.approx(
        (result["player_age"] - result["opponent_age"]).tolist()
    )
    assert download.call_count == 3


def test_get_career_matches_rejects_unknown_player(monkeypatch):
    download = Mock(return_value=DIRECTORY)
    monkeypatch.setattr("tennis_career.api._download_text", download)
    with pytest.raises(ValueError, match="Player not found"):
        get_career_matches("GastonSanchez")
    download.assert_called_once_with(f"{BASE_URL}/mwplayerlist.js")