"""
load.py

Loads the synthetic roster and event sign-in sheets, mirroring the logic
from the original Apps Script (header on row 6 of the roster, one CSV per
event with an "ID Number" column).
"""

from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
EVENTS_DIR = DATA_DIR / "events"

BUILDING_MAP = {
    "GORH": "Gough", "SPRH": "Sparrowk", "DOAN": "Doane", "EARH": "Eagle",
    "HARH": "Hainer", "GARH": "Gallup", "KERH": "Kea", "GFRH": "Guffin",
}


def load_roster() -> pd.DataFrame:
    """Load the synthetic roster, skipping the 5 blank rows so row 6 is
    treated as the header — mirrors the original sheet's layout."""
    df = pd.read_csv(DATA_DIR / "students.csv", skiprows=5)

    # Drop the synthetic-data-only propensity column if present; the real
    # pipeline should never see it, since it didn't exist in the original tool.
    df = df.drop(columns=["_engagement_propensity"], errors="ignore")

    df["Student ID"] = pd.to_numeric(df["Student ID"], errors="coerce")
    df = df.dropna(subset=["Student ID"])
    df["Student ID"] = df["Student ID"].astype(int)

    # Normalize building codes -> friendly names (mirrors BUILDING_MAP)
    df["Res Building"] = df["Res Building"].fillna("").astype(str).str.strip()
    df["Res Building"] = df["Res Building"].apply(lambda b: BUILDING_MAP.get(b, b))

    # Commuter override, same rule as original: On-Campus Housing == "N" -> Commuter
    df["Housing"] = df.apply(
        lambda r: "Commuter" if r["On-Campus Housing"] == "N" else (r["Res Building"] or "Unknown"),
        axis=1,
    )

    return df.set_index("Student ID", drop=False)


def load_events() -> dict[str, pd.DataFrame]:
    """Load each event CSV into a DataFrame keyed by event name."""
    events = {}
    for path in sorted(EVENTS_DIR.glob("*.csv")):
        df = pd.read_csv(path)
        if "ID Number" not in df.columns:
            continue
        df["ID Number"] = pd.to_numeric(df["ID Number"], errors="coerce")
        df = df.dropna(subset=["ID Number"])
        df["ID Number"] = df["ID Number"].astype(int)
        # de-duplicate same student signing in twice at one event
        df = df.drop_duplicates(subset="ID Number")
        event_name = path.stem.replace("_", " ")
        events[event_name] = df
    return events


def build_attendance_table(roster: pd.DataFrame, events: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Returns roster with an added 'events_attended' count and a per-event
    boolean column, mirroring the eventsCount logic in the original script."""
    roster = roster.copy()
    roster["events_attended"] = 0

    for event_name, ev_df in events.items():
        attended_ids = set(ev_df["ID Number"])
        col_name = f"attended::{event_name}"
        roster[col_name] = roster["Student ID"].isin(attended_ids)
        roster["events_attended"] += roster[col_name].astype(int)

    return roster
