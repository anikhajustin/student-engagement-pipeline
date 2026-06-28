"""
charts.py

Generates the matplotlib/seaborn charts used in the public case study page.
All charts run on synthetic data only.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

OUTPUT_DIR = Path(__file__).parent / "output" / "figures"
MAROON = "#6B0000"
GOLD = "#C9A227"

sns.set_theme(style="whitegrid")


def _save(fig, name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved chart: {path}")
    return path


def chart_event_attendance_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["Events Attended"].astype(str), df["Number of Students"], color=MAROON)
    ax.set_xlabel("Number of Events Attended")
    ax.set_ylabel("Number of Students")
    ax.set_title("Distribution of Event Attendance (Synthetic Data)")
    return _save(fig, "fig1_attendance_distribution.png")


def chart_by_class_year(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(df["Class Year"], df["Attendees"], color=MAROON)
    ax.set_ylabel("Attendees")
    ax.set_title("Attendance by Class Year (Synthetic Data)")
    return _save(fig, "fig2_by_class_year.png")


def chart_residence_hall_participation(df: pd.DataFrame):
    df = df.dropna(subset=["Participation Rate (%)"]).sort_values("Participation Rate (%)", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["Residence Hall"], df["Participation Rate (%)"], color=GOLD)
    ax.set_ylabel("Participation Rate (%)")
    ax.set_title("Participation Rate by Residence Hall (Synthetic Data)")
    plt.xticks(rotation=30, ha="right")
    return _save(fig, "fig3_residence_hall_participation.png")


def chart_engagement_summary(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = [MAROON, "#A33", GOLD, "#2E7D32"]
    ax.pie(df["Students"], labels=df["Engagement Level"], autopct="%1.0f%%",
           colors=colors, startangle=90)
    ax.set_title("Engagement Level Distribution (Synthetic Data)")
    return _save(fig, "fig4_engagement_distribution.png")


def chart_engagement_by_class(df: pd.DataFrame):
    levels = ["No Engagement", "Low Engagement", "Moderate Engagement", "High Engagement"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = [0] * len(df)
    colors = [MAROON, "#A33", GOLD, "#2E7D32"]
    for level, color in zip(levels, colors):
        ax.bar(df["Class Year"], df[level], bottom=bottom, label=level, color=color)
        bottom = [b + v for b, v in zip(bottom, df[level])]
    ax.set_ylabel("Number of Students")
    ax.set_title("Engagement Level by Class Year (Synthetic Data)")
    ax.legend()
    return _save(fig, "fig5_engagement_by_class.png")


def generate_all_charts(breakdowns: dict, engagement_summary: pd.DataFrame,
                         engagement_by_class: pd.DataFrame):
    chart_event_attendance_distribution(breakdowns["Event Attendance"])
    chart_by_class_year(breakdowns["By Class Year"])
    chart_residence_hall_participation(breakdowns["By Residence Hall"])
    chart_engagement_summary(engagement_summary)
    chart_engagement_by_class(engagement_by_class)
