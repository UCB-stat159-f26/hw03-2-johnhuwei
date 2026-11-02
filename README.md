# Tennis Career

A Python package for retrieving tennis match data from Tennis Abstract and plotting match outcomes by player age and age difference with opponents.

## Installation

Requires Python 3.9 or later.

Install directly from GitHub:

```bash
python -m pip install git+https://github.com/UCB-stat159-f26/hw03-2-johnhuwei.git
```

Access to the repository is required if it is private.

For local development, run these commands from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

```python
import matplotlib.pyplot as plt
from tennis_career import get_career_matches, plot_career_matches

serena = get_career_matches("serena williams")
ax = plot_career_matches(serena)
ax.figure.savefig("serena_matches.png", dpi=150, bbox_inches="tight")
plt.show()

rafa = get_career_matches("RafaelNadal")
ax = plot_career_matches(rafa)
plt.show()
```

Names are matched without regard to case or whitespace. For example, `"serena williams"`, `"Serena Williams"`, and `"SerenaWilliams"` identify the same player.

## Public functions

### `get_career_matches(player_name)`

Retrieves the player directory, resolves the player's name, and downloads
match data. Historical records are included when the source indicates
that an additional career file is required.

Returns a pandas DataFrame sorted by date, with duplicate cleaned rows removed:

| Column | Meaning |
| --- | --- |
| `date` | Date recorded by Tennis Abstract |
| `tournament` | Tournament name |
| `surface` | Court surface |
| `result` | Match result, such as `W` or `L` |
| `opponent` | Opponent name |
| `opponent_age` | Opponent age in years |
| `player_age` | Player age in years |
| `age_difference` | Player age minus opponent age |

The official player name is stored in `matches.attrs["player_name"]`.

An unknown player raises `ValueError` with a descriptive message:

```python
get_career_matches("GastonSanchez")
```

Network failures raise `ConnectionError`. Missing source files or invalid
source data can raise `ValueError`.

### `plot_career_matches(matches)`

Returns a Matplotlib `Axes` object. The horizontal axis shows player age;
the vertical axis shows age difference. Positive differences mean the
player is older than the opponent. Wins are blue and losses are purple.

The function does not automatically display or save the figure. Use
`plt.show()` or `ax.figure.savefig(...)`.

## Data conventions and limitations

- Data comes from [Tennis Abstract](https://www.tennisabstract.com/).
- Ages derived from birth dates use elapsed days divided by 365.25.
  Numeric opponent ages supplied by the source are retained.
- Dates are used as recorded by the source and may represent tournament
  dates rather than the exact day of each match.
- Coverage and accuracy depend on the source. Records are not independently
  verified or removed based on assumptions about a player's career.
- Source format changes may require updates to the package.
- Missing or invalid age information may stop processing with an error.
- The plot displays records labeled `W` or `L`.

## Tests

From the repository root, with development dependencies installed:

```bash
python -m pytest -q
```

Automated tests use local fixtures and mocked downloads without contacting live servers. They cover parsing, age calculations, name matching, download errors, historical-data merging, and plotting.

Real-player downloads and plot inspection are performed separately as manual checks.