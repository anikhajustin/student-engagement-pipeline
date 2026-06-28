# Student Engagement Pipeline

A Python rebuild of an institutional event attendance and engagement reporting
tool, originally built in Google Apps Script for a university student
engagement office. This project replicates the original tool's analysis
logic and adds a new rule-based engagement flagging layer, using entirely
**synthetic data**.

> **Data notice:** All data in this repository (`data/`) is synthetically
> generated and does not represent real students, attendance records, or
> institutional data. The original tool processes real student records and
> is used in production at a university; that data and that code are not
> public. This repository demonstrates the *rebuilt pipeline's* architecture
> and output format only.

## Background

The original tool lived inside a Google Sheet: a student roster tab plus one
tab per campus event, with an Apps Script macro that joined them, counted
attendance, and generated 11 formatted report tabs with charts (by class
year, residence hall, major, race/ethnicity, first-generation status, Pell
Grant status, and more). It replaced a multi-hour manual cross-tabbing
process each semester and has been used to brief university leadership on
event participation trends.

This project re-architects that tool as a Python pipeline (pandas +
matplotlib + openpyxl), and adds a capability the original tool didn't have:
a transparent, rule-based engagement flag that surfaces which students may
be disengaging — not just how many people attended each event.

## What's in this repo

| File | Purpose |
|---|---|
| `generate_synthetic_data.py` | Generates a fake student roster + event sign-in sheets matching the original schema |
| `load.py` | Loads roster/event data, mirrors original sheet quirks (header row offset, building code mapping) |
| `analysis.py` | The 11 demographic breakdowns from the original tool, rebuilt in pandas |
| `flagging.py` | **New capability** — rule-based engagement flag (0 / 1–2 / 3–4 / 5+ events attended) |
| `export_excel.py` | Produces a downloadable multi-sheet Excel workbook |
| `charts.py` | Produces the chart images used in the project case study |
| `main.py` | Runs the full pipeline end to end |

## Why a flagging layer was added

The original tool was purely descriptive — it counted and broke down
attendance, but never identified which individual students might need
outreach. Adding a flag turns the tool from "how many people came" into
"who might be falling through the cracks," which is the more actionable
question for a student engagement office. The logic is deliberately simple
and count-based (not a predictive model) so any staff member can audit
exactly why a student received a given flag — important for a tool used in
real decisions about real students.

## Why counts instead of percentages

Early design used percentage-of-events-attended as the threshold, but with a
small number of tracked events per semester, percentages shift meaning
depending on how many events happened to be tracked that term (2 of 8
events = 25%, but 2 of 15 events = 13% — the same real-world behavior gets a
different label). Fixed event counts give a stable rule that means the same
thing every semester and is easy to explain to non-technical staff.

## Running it yourself

```bash
pip install -r requirements.txt
python generate_synthetic_data.py   # creates data/students.csv and data/events/*.csv
python main.py                      # runs the full pipeline
```

Output lands in `output/`: a multi-sheet Excel workbook and a set of chart
PNGs.

## Tools used

Python, pandas, matplotlib, seaborn, openpyxl, Faker (for synthetic data
generation)

## Full case study

A full write-up with sample charts and findings (using synthetic data) is
available on my portfolio: [anikhajustin.github.io](https://anikhajustin.github.io)
