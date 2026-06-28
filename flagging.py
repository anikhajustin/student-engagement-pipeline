"""
flagging.py

NEW CAPABILITY — did not exist in the original Apps Script tool.

The original tool was purely descriptive (counts and breakdowns). This module
adds a simple, transparent, rule-based engagement flag so the tool can
surface which students may be disengaging, not just how many events
happened in total.

Deliberately rule-based (not a predictive model) so the logic is fully
auditable by any staff member reviewing the output — appropriate for an
institutional reporting tool where decisions affect real students.
"""

import pandas as pd


def add_engagement_flags(roster: pd.DataFrame, total_events: int) -> pd.DataFrame:
    """
    Adds two columns:
      - engagement_rate: events_attended / total_events_tracked (kept for
        reference/reporting, but NOT used to set the flag — see note below)
      - engagement_flag: categorical engagement flag based on fixed event
        COUNTS, not percentages.

    Why counts instead of percentages: with a small number of tracked events
    per semester, percentage thresholds shift meaning depending on how many
    events happened to be tracked that term (e.g. 2 of 8 events = 25%, but
    2 of 15 events = 13% — same real-world behavior, different label). Fixed
    counts give a stable, plain-language rule that means the same thing every
    semester and is easy to explain to non-technical staff: "attended at
    least 3 events this semester."

    Thresholds (transparent, adjustable as semesters provide more data):
      - "No Engagement"      : attended 0 events
      - "Low Engagement"     : attended 1-2 events
      - "Moderate Engagement": attended 3-4 events
      - "High Engagement"    : attended 5+ events
    """
    roster = roster.copy()

    roster["engagement_rate"] = (
        (roster["events_attended"] / total_events).round(3) if total_events else 0.0
    )

    def flag(count: int) -> str:
        if count == 0:
            return "No Engagement"
        elif count <= 2:
            return "Low Engagement"
        elif count <= 4:
            return "Moderate Engagement"
        else:
            return "High Engagement"

    roster["engagement_flag"] = roster["events_attended"].apply(flag)
    return roster


def engagement_summary(roster: pd.DataFrame) -> pd.DataFrame:
    """Summary table: how many students fall into each flag category,
    broken down further by class year so staff can see whether disengagement
    clusters in a particular cohort (e.g. first-years)."""
    order = ["No Engagement", "Low Engagement", "Moderate Engagement", "High Engagement"]

    counts = roster["engagement_flag"].value_counts().reindex(order, fill_value=0)
    df = counts.reset_index()
    df.columns = ["Engagement Level", "Students"]
    df["% of Roster"] = (df["Students"] / len(roster) * 100).round(1)
    return df


def engagement_by_class_year(roster: pd.DataFrame) -> pd.DataFrame:
    order = ["No Engagement", "Low Engagement", "Moderate Engagement", "High Engagement"]
    class_order = ["FR", "SO", "JR", "SR"]
    class_labels = {"FR": "Freshman", "SO": "Sophomore", "JR": "Junior", "SR": "Senior"}

    pivot = pd.crosstab(roster["Class"], roster["engagement_flag"])
    pivot = pivot.reindex(index=class_order, columns=order, fill_value=0)
    pivot.index = [class_labels[c] for c in pivot.index]
    pivot.index.name = "Class Year"
    return pivot.reset_index()
