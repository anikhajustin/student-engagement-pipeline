"""
main.py

Runs the full pipeline end to end:
  1. Load synthetic roster + event sign-in sheets
  2. Build attendance table
  3. Run all demographic breakdowns (mirrors original Apps Script tabs)
  4. Add NEW engagement flagging layer (did not exist in the original tool)
  5. Export multi-sheet Excel workbook (downloadable artifact)
  6. Export charts (used in the public case study page)

Run with: python main.py
"""

from load import load_roster, load_events, build_attendance_table
from analysis import run_all_breakdowns
from flagging import add_engagement_flags, engagement_summary, engagement_by_class_year
from export_excel import export_to_excel
from charts import generate_all_charts


def main():
    print("Loading synthetic roster and events...")
    roster = load_roster()
    events = load_events()

    print(f"Loaded {len(roster)} students, {len(events)} events.")

    roster = build_attendance_table(roster, events)

    print("Running demographic breakdowns...")
    breakdowns = run_all_breakdowns(roster, events)

    print("Computing engagement flags (new capability)...")
    roster = add_engagement_flags(roster, total_events=len(events))
    eng_summary = engagement_summary(roster)
    eng_by_class = engagement_by_class_year(roster)

    print("Exporting Excel workbook...")
    export_to_excel(breakdowns, eng_summary, eng_by_class)

    print("Generating charts for case study page...")
    generate_all_charts(breakdowns, eng_summary, eng_by_class)

    print("\nPipeline complete.")
    print("All data used above is synthetically generated.")


if __name__ == "__main__":
    main()
