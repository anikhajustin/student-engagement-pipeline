"""
analysis.py

Mirrors each buildX() breakdown from the original Apps Script, but as
pandas groupby/aggregation logic instead of manual sheet-writing code.
"""

import pandas as pd

CLASS_LABELS = {"FR": "Freshman", "SO": "Sophomore", "JR": "Junior", "SR": "Senior"}


def summary_metrics(roster: pd.DataFrame, events: dict) -> dict:
    total_students = len(roster)
    attendees = roster[roster["events_attended"] > 0]
    total_attendees = len(attendees)
    total_events = len(events)
    total_swipes = sum(len(df) for df in events.values())

    return {
        "Total Undergraduate Students": total_students,
        "Attended >= 1 Event": total_attendees,
        "Did NOT Attend Any Event": total_students - total_attendees,
        "Total Event Attendances (all swipes)": total_swipes,
        "Total Events Tracked": total_events,
    }


def event_attendance_distribution(roster: pd.DataFrame) -> pd.DataFrame:
    """How many events did each student attend? (mirrors buildEventAttendance)"""
    dist = roster["events_attended"].value_counts().sort_index()
    out = dist.reset_index()
    out.columns = ["Events Attended", "Number of Students"]
    out["% of All Students"] = (out["Number of Students"] / len(roster) * 100).round(1)
    return out


def by_class_year(attendees: pd.DataFrame) -> pd.DataFrame:
    counts = attendees["Class"].value_counts()
    rows = []
    for code in ["FR", "SO", "JR", "SR"]:
        cnt = int(counts.get(code, 0))
        rows.append({"Class Year": CLASS_LABELS[code], "Attendees": cnt})
    df = pd.DataFrame(rows)
    df["% of Attendees"] = (df["Attendees"] / len(attendees) * 100).round(1)
    return df


def commuters_vs_oncampus(attendees: pd.DataFrame) -> pd.DataFrame:
    on_campus = (attendees["Housing"] != "Commuter").sum()
    commuter = (attendees["Housing"] == "Commuter").sum()
    df = pd.DataFrame({
        "Housing Type": ["On-Campus Housing", "Commuter"],
        "Attendees": [int(on_campus), int(commuter)],
    })
    df["% of Attendees"] = (df["Attendees"] / len(attendees) * 100).round(1)
    return df


def by_residence_hall(attendees: pd.DataFrame, roster: pd.DataFrame) -> pd.DataFrame:
    att_counts = attendees["Housing"].value_counts()
    tot_counts = roster["Housing"].value_counts()
    buildings = sorted(b for b in att_counts.index if b != "Commuter")
    if "Commuter" in att_counts.index:
        buildings.append("Commuter")

    rows = []
    for b in buildings:
        att = int(att_counts.get(b, 0))
        tot = int(tot_counts.get(b, 0))
        rate = round(att / tot * 100, 1) if tot else None
        rows.append({"Residence Hall": b, "Attendees": att, "Total Students": tot,
                      "Participation Rate (%)": rate})
    return pd.DataFrame(rows)


def by_major(attendees: pd.DataFrame) -> pd.DataFrame:
    counts = attendees["Program Title"].value_counts()
    df = counts.reset_index()
    df.columns = ["Major / Program", "Attendees"]
    df["% of Attendees"] = (df["Attendees"] / len(attendees) * 100).round(1)
    return df


def by_demographic(attendees: pd.DataFrame, column: str, label: str) -> pd.DataFrame:
    """Generic breakdown for race/ethnicity, gender, etc."""
    counts = attendees[column].value_counts()
    df = counts.reset_index()
    df.columns = [label, "Attendees"]
    df["% of Attendees"] = (df["Attendees"] / len(attendees) * 100).round(1)
    return df


def by_yes_no(attendees: pd.DataFrame, column: str, yes_label: str, no_label: str) -> pd.DataFrame:
    """Generic Y/N breakdown for first-gen, Pell, athlete, etc."""
    yes = (attendees[column] == "Y").sum()
    no = (attendees[column] == "N").sum()
    df = pd.DataFrame({
        "Category": [yes_label, no_label],
        "Attendees": [int(yes), int(no)],
    })
    df["% of Attendees"] = (df["Attendees"] / len(attendees) * 100).round(1)
    return df


def run_all_breakdowns(roster: pd.DataFrame, events: dict) -> dict[str, pd.DataFrame]:
    attendees = roster[roster["events_attended"] > 0]

    return {
        "Summary": pd.DataFrame(list(summary_metrics(roster, events).items()),
                                 columns=["Metric", "Count"]),
        "Event Attendance": event_attendance_distribution(roster),
        "By Class Year": by_class_year(attendees),
        "Commuters vs On-Campus": commuters_vs_oncampus(attendees),
        "By Residence Hall": by_residence_hall(attendees, roster),
        "By Major": by_major(attendees),
        "Race & Ethnicity": by_demographic(attendees, "Race/Ethnicity", "Race/Ethnicity"),
        "First Gen": by_yes_no(attendees, "First Generation", "First Gen", "Non-First Gen"),
        "Pell Grant": by_yes_no(attendees, "Rec'd Pell", "Received Pell Grant", "Did Not Receive"),
        "Gender": by_demographic(attendees, "Gender", "Gender"),
        "Athlete vs Non-Athlete": by_yes_no(attendees, "ATHLETE", "Student Athlete", "Non-Athlete"),
    }
