"""
generate_synthetic_data.py

Generates a synthetic student roster + event sign-in sheets that mirror the
STRUCTURE of the original Google Sheets tool (StudentList + per-event sheets),
WITHOUT using any real student data. All names, IDs, and demographic values
are randomly generated and have no connection to real individuals.

Output:
    data/students.csv          (synthetic roster, mirrors "StudentList" tab)
    data/events/*.csv          (synthetic event sign-in sheets)
"""

import csv
import random
from pathlib import Path
from faker import Faker

fake = Faker()
random.seed(42)  # reproducible synthetic dataset

# ── CONFIG ────────────────────────────────────────────────────────────────
N_STUDENTS = 450
OUTPUT_DIR = Path(__file__).parent / "data"
EVENTS_DIR = OUTPUT_DIR / "events"

CLASS_YEARS = ["FR", "SO", "JR", "SR"]
BUILDINGS = ["Gough", "Sparrowk", "Doane", "Eagle", "Hainer", "Gallup", "Kea", "Guffin"]
MAJORS = [
    "Computer Science", "Biology", "Business Administration", "Psychology",
    "Nursing", "Communications", "Education", "Criminal Justice",
    "Data Science", "Mechanical Engineering", "Exercise Science", "English",
]
RACE_ETHNICITY = [
    "White", "Black or African American", "Hispanic or Latino", "Asian",
    "Two or More Races", "American Indian or Alaska Native", "Unknown",
]
GENDERS = ["M", "F"]
YES_NO_WEIGHTS = {  # P(Y)
    "on_campus": 0.55,
    "first_gen": 0.30,
    "pell": 0.35,
    "athlete": 0.15,
}

EVENT_NAMES = [
    "Welcome Week Kickoff",
    "Fall Career Fair",
    "Diversity & Inclusion Panel",
    "Study Skills Workshop",
    "Homecoming Tailgate",
    "Wellness Fair",
    "Late Night Trivia",
    "Spring Involvement Expo",
]

# Roughly how likely a given student is to attend a given event,
# with some students being "highly engaged" and others "rarely engaged"
# so the resulting distribution looks realistic.
def student_engagement_propensity():
    # Most students cluster low-to-mid; a smaller group is highly engaged
    return random.choices(
        [0.05, 0.15, 0.35, 0.6, 0.85],
        weights=[30, 30, 20, 12, 8],
        k=1,
    )[0]


def weighted_yn(p_yes):
    return "Y" if random.random() < p_yes else "N"


def generate_roster():
    rows = []
    for sid in range(100000, 100000 + N_STUDENTS):
        on_campus = weighted_yn(YES_NO_WEIGHTS["on_campus"])
        row = {
            "Student ID": sid,
            "Class": random.choice(CLASS_YEARS),
            "Res Building": random.choice(BUILDINGS) if on_campus == "Y" else "",
            "On-Campus Housing": on_campus,
            "Program Title": random.choice(MAJORS),
            "Race/Ethnicity": random.choice(RACE_ETHNICITY),
            "Gender": random.choice(GENDERS),
            "First Generation": weighted_yn(YES_NO_WEIGHTS["first_gen"]),
            "Rec'd Pell": weighted_yn(YES_NO_WEIGHTS["pell"]),
            "ATHLETE": weighted_yn(YES_NO_WEIGHTS["athlete"]),
            "_engagement_propensity": round(student_engagement_propensity(), 2),
        }
        rows.append(row)
    return rows


def write_roster(rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "students.csv"

    # Mirrors original sheet layout: header on row 6 -> we pad with 5 blank
    # rows above the header so the loader logic matches the original
    # ("header is on row 6, data starts row 7").
    fieldnames = [
        "Student ID", "Class", "Res Building", "On-Campus Housing",
        "Program Title", "Race/Ethnicity", "Gender", "First Generation",
        "Rec'd Pell", "ATHLETE", "_engagement_propensity",
    ]

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for _ in range(5):
            writer.writerow([])  # blank rows 1-5, matching original sheet quirk
        writer.writerow(fieldnames)  # row 6 = header
        for row in rows:
            writer.writerow([row[k] for k in fieldnames])

    print(f"Wrote roster: {path} ({len(rows)} students)")
    return path


def generate_events(roster_rows):
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    for event_name in EVENT_NAMES:
        attendees = []
        for student in roster_rows:
            if random.random() < student["_engagement_propensity"]:
                attendees.append(student["Student ID"])

        random.shuffle(attendees)
        path = EVENTS_DIR / f"{event_name.replace(' ', '_')}.csv"
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID Number", "Timestamp"])
            for sid in attendees:
                writer.writerow([sid, fake.date_time_this_year().isoformat()])

        print(f"Wrote event: {path} ({len(attendees)} attendees)")


if __name__ == "__main__":
    roster_rows = generate_roster()
    write_roster(roster_rows)
    generate_events(roster_rows)
    print("\nSynthetic data generation complete.")
    print("NOTE: all IDs, demographics, and attendance are randomly generated.")
    print("No real student data was used or referenced.")
