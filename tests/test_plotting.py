"""Test plotting with local example data."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennis_career import plot_career_matches


def test_plot_career_matches_draws_wins_and_losses():
    matches = pd.DataFrame({
        "player_age": [20.0, 21.0, 22.0],
        "age_difference": [2.0, -3.0, 1.0],
        "result": ["W", "L", "W"],
    })
    matches.attrs["player_name"] = "Example Player"
    ax = plot_career_matches(matches)
    try:
        assert ax.collections[0].get_offsets().tolist() == [[20.0, 2.0], [22.0, 1.0]]
        assert ax.collections[1].get_offsets().tolist() == [[21.0, -3.0]]
        assert "Example Player" in ax.get_title()
        assert ax.xaxis.get_ticks_position() == "top"
    finally:
        plt.close(ax.figure)


def test_plot_career_matches_rejects_missing_columns():
    with pytest.raises(ValueError, match="requires"):
        plot_career_matches(pd.DataFrame({"result": ["W"]}))


def test_plot_career_matches_rejects_empty_data():
    matches = pd.DataFrame(columns=["player_age", "age_difference", "result"])
    with pytest.raises(ValueError, match="empty"):
        plot_career_matches(matches)