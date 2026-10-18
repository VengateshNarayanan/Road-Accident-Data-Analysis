
import pandas as pd

from config import (
    NAME_COLUMN,
    SERIAL_COLUMN,
    METRICS,
    ACCIDENT_CATEGORIES,
)


def filter_geography(df, geography):
    return df[df["Geography"] == geography].copy()


def get_available_states(df):
    states = df[df["Geography"] == "State / UT"][NAME_COLUMN]
    return sorted(states.dropna().unique().tolist())


def get_summary_cards(df):
    if df.empty:
        return {
            "Accident Cases": 0,
            "People Injured": 0,
            "Deaths": 0,
        }

    return {
        "Accident Cases": int(
            df["Total Traffic Accidents - Cases"].sum()
        ),
        "People Injured": int(
            df["Total Traffic Accidents - Injured"].sum()
        ),
        "Deaths": int(
            df["Total Traffic Accidents - Died"].sum()
        ),
    }


def sort_by_metric(df, metric_name, top_n=10):
    column = METRICS[metric_name]

    return (
        df.sort_values(column, ascending=False)
        .head(top_n)
        .copy()
    )


def get_state_data(df, state_name):
    selected = df[
        (df["Geography"] == "State / UT")
        & (df[NAME_COLUMN] == state_name)
    ].copy()

    return selected


def get_category_totals(df):
    rows = []

    for category, columns in ACCIDENT_CATEGORIES.items():
        rows.append({
            "Category": category,
            "Cases": int(df[columns["cases"]].sum()),
            "Injured": int(df[columns["injured"]].sum()),
            "Deaths": int(df[columns["deaths"]].sum()),
        })

    return pd.DataFrame(rows)


def get_heatmap_matrix(df):
    categories = get_category_totals(df)

    if categories.empty:
        return pd.DataFrame()

    matrix = categories.set_index("Category")[
        ["Cases", "Injured", "Deaths"]
    ]

    # Normalize each column independently to show relative
    # patterns, not direct comparisons of raw quantities.
    maximums = matrix.max(axis=0).replace(0, 1)

    return matrix.div(maximums, axis=1)
