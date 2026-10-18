
import pandas as pd

from config import DATA_FILE, NAME_COLUMN, SERIAL_COLUMN


def load_data():
    try:
        df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_FILE, encoding="latin1")

    df.columns = df.columns.str.strip()

    required_columns = [
        NAME_COLUMN,
        SERIAL_COLUMN,
        "Total Traffic Accidents - Cases",
        "Total Traffic Accidents - Injured",
        "Total Traffic Accidents - Died",
        "Road Accidents - Cases",
        "Road Accidents - Injured",
        "Road Accidents - Died",
        "Railway Accidents - Cases",
        "Railway Accidents - Injured",
        "Railway Accidents - Died",
        "Railway Crossing Accidents - Cases",
        "Railway Crossing Accidents - Injured",
        "Railway Crossing Accidents - Died",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            "The CSV is missing these required columns:\n"
            + "\n".join(missing)
        )

    # Convert serial numbers to numeric values.
    df[SERIAL_COLUMN] = pd.to_numeric(
        df[SERIAL_COLUMN], errors="coerce"
    )

    # Remove total/subtotal rows and invalid serial numbers.
    df = df.dropna(subset=[SERIAL_COLUMN]).copy()

    # This dataset uses serials 1–36 for states/UTs and
    # 37–89 for cities. Summary rows have non-numeric serials.
    df = df[df[SERIAL_COLUMN].between(1, 89)].copy()

    # Convert accident statistics to numeric values.
    metric_columns = [
        col for col in required_columns
        if col not in [NAME_COLUMN, SERIAL_COLUMN]
    ]

    for column in metric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)

    df[SERIAL_COLUMN] = df[SERIAL_COLUMN].astype(int)

    df["Geography"] = df[SERIAL_COLUMN].apply(
        lambda number: "State / UT"
        if 1 <= number <= 36
        else "City"
    )

    df = df.sort_values(SERIAL_COLUMN).reset_index(drop=True)

    return df
