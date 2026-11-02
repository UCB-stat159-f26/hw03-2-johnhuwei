"""Plot tennis career results by age."""

import matplotlib.pyplot as plt


def _style_axes(ax, player_name):
    """Apply labels and styling to the career plot."""
    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xlabel("Player age (years)")
    ax.xaxis.set_label_position("top")
    ax.xaxis.tick_top()
    ax.set_ylabel("Age difference (years): player − opponent")
    ax.set_title(f"{player_name}: career match results", pad=45)
    ax.set_axisbelow(True)
    ax.grid(color="#E6E6E6", linewidth=1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(frameon=False)


def plot_career_matches(matches):
    """Plot cleaned career matches and return the Matplotlib Axes."""
    required = {"player_age", "age_difference", "result"}
    if not required.issubset(matches.columns):
        raise ValueError("Match data requires player_age, age_difference, and result.")
    if matches.empty:
        raise ValueError("Match data is empty.")
    fig, ax = plt.subplots(figsize=(12, 7))
    for outcome, color, label in [
        ("W", "#40C4E5", "Won"),
        ("L", "#96368D", "Lost"),
    ]:
        subset = matches.loc[matches["result"] == outcome]
        ax.scatter(
            subset["player_age"], subset["age_difference"],
            color=color, label=label, s=20, alpha=0.8, edgecolors="none",
        )
    _style_axes(ax, matches.attrs.get("player_name", "Player"))
    fig.tight_layout()
    return ax