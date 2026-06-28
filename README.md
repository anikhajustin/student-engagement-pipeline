# Student Engagement Analytics Pipeline

An automated analytics pipeline that processes campus event attendance data to surface student engagement patterns, demographic participation trends, and where outreach should be targeted, built to solve a real need for a university student engagement office.

> **Data notice:** All data in this repository (`data/`) is synthetically generated and does not represent real students, attendance records, or institutional data. The production version of this tool processes real student records and has been used to brief university leadership; that data is not public. This repository demonstrates the pipeline's architecture and output format using synthetic data only.

## Background

As a Micro-Intern in the Student Engagement department, I was asked to help answer a practical question: who is engaging with campus events, who isn't, and where should outreach and resources be targeted. Previously, answering that question meant hours of manual cross-tabbing in a spreadsheet every semester: pulling a roster, cross-referencing it against sign-in sheets from each event, and manually building breakdowns by class year, housing, major, and other demographics.

## What the pipeline does

1. **Ingests** a student roster and a set of per-event sign-in sheets
2. **Joins and counts** attendance per student across all tracked events
3. **Breaks down participation** across 10+ dimensions: class year, housing type, residence hall, major, race/ethnicity, gender, first-generation status, Pell Grant status, and athlete status
4. **Flags engagement level** for every student on the roster, using a transparent, rule-based system (see below), including students who attended zero events, the group most actionable for outreach
5. **Outputs** a multi-sheet Excel workbook (the institutional deliverable) and a set of charts (for reporting and presentation)

## What's in this repo

| File | Purpose |
|---|---|
| `generate_synthetic_data.py` | Generates a fake student roster + event sign-in sheets for public demonstration |
| `load.py` | Loads and cleans roster/event data |
| `analysis.py` | Computes the demographic participation breakdowns |
| `flagging.py` | Computes the engagement flag for every student |
| `export_excel.py` | Produces the downloadable multi-sheet Excel workbook |
| `charts.py` | Produces the chart images used in the project case study |
| `main.py` | Runs the full pipeline end to end |

## The engagement flag

Every student on the roster is flagged based on the number of events they attended that semester:

- **No Engagement**: attended 0 events
- **Low Engagement**: attended 1 to 2 events
- **Moderate Engagement**: attended 3 to 4 events
- **High Engagement**: attended 5+ events

Fixed event counts were used instead of percentages so the rule stays simple, stable across semesters regardless of how many events are tracked, and easy for non-technical staff to interpret and act on.

## Running it yourself

```bash
pip install -r requirements.txt
python generate_synthetic_data.py   # creates data/students.csv and data/events/*.csv
python main.py                      # runs the full pipeline
```

Output lands in `output/`: a multi-sheet Excel workbook and a set of chart PNGs.

## Tools used

Python, pandas, matplotlib, seaborn, openpyxl, Faker (for synthetic data generation)

## Full case study

A full write-up with sample charts and findings (using synthetic data) is available on my portfolio: [anikhajustin.github.io](https://anikhajustin.github.io)
