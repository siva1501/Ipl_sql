"""Generate and save PNG charts for SQL queries if matplotlib is installed."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db" / "ipl.db"
QUERIES_DIR = BASE_DIR / "queries"
OUTPUTS_DIR = BASE_DIR / "outputs"


def generate_plots():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed. To generate PNG charts, run:")
        print("    pip install matplotlib")
        return

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Total runs by team
    cursor.execute((QUERIES_DIR / "1_total_runs_by_team.sql").read_text())
    rows = cursor.fetchall()
    teams, runs = [r[0] for r in rows], [r[1] for r in rows]
    plt.figure(figsize=(12, 6))
    plt.bar(teams, runs, color="skyblue")
    plt.title("Total Runs Scored by Each Team in IPL", fontweight="bold")
    plt.xlabel("Team")
    plt.ylabel("Total Runs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "1_total_runs_by_team.png")
    plt.close()
    print("✓ Saved outputs/1_total_runs_by_team.png")

    # 2. Top 10 RCB Batsmen
    cursor.execute((QUERIES_DIR / "2_top_10_rcb_batsmen.sql").read_text())
    rows = cursor.fetchall()
    batsmen, runs = [r[0] for r in rows], [r[1] for r in rows]
    plt.figure(figsize=(12, 6))
    plt.bar(batsmen, runs, color="crimson")
    plt.title("Top 10 Batsmen for Royal Challengers Bangalore", fontweight="bold")
    plt.xlabel("Batsman")
    plt.ylabel("Total Runs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "2_top_10_rcb_batsmen.png")
    plt.close()
    print("✓ Saved outputs/2_top_10_rcb_batsmen.png")

    # 3. Foreign Umpires by Country
    cursor.execute((QUERIES_DIR / "3_foreign_umpire_analysis.sql").read_text())
    rows = cursor.fetchall()
    countries, counts = [r[0] for r in rows], [r[1] for r in rows]
    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color="teal")
    plt.title("Number of Foreign Umpires in IPL", fontweight="bold")
    plt.xlabel("Country")
    plt.ylabel("Number of Umpires")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "3_foreign_umpire_analysis.png")
    plt.close()
    print("✓ Saved outputs/3_foreign_umpire_analysis.png")

    # 5. Matches per year
    cursor.execute((QUERIES_DIR / "5_matches_played_per_year.sql").read_text())
    rows = cursor.fetchall()
    years, counts = [str(r[0]) for r in rows], [r[1] for r in rows]
    plt.figure(figsize=(10, 5))
    plt.bar(years, counts, color="orange")
    plt.title("Number of Matches Played per Year in IPL", fontweight="bold")
    plt.xlabel("Year")
    plt.ylabel("Total Matches")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "5_matches_played_per_year.png")
    plt.close()
    print("✓ Saved outputs/5_matches_played_per_year.png")

    # 7. Extra runs 2016
    cursor.execute((QUERIES_DIR / "7_extra_runs_conceded_2016.sql").read_text())
    rows = cursor.fetchall()
    teams, runs = [r[0] for r in rows], [r[1] for r in rows]
    plt.figure(figsize=(12, 6))
    plt.bar(teams, runs, color="coral")
    plt.title("Extra Runs Conceded per Team in IPL 2016", fontweight="bold")
    plt.xlabel("Team")
    plt.ylabel("Extra Runs Conceded")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "7_extra_runs_conceded_2016.png")
    plt.close()
    print("✓ Saved outputs/7_extra_runs_conceded_2016.png")

    # 8. Economical Bowlers 2015
    cursor.execute((QUERIES_DIR / "8_top_10_economical_bowlers_2015.sql").read_text())
    rows = cursor.fetchall()
    bowlers, economy = [r[0] for r in rows], [r[3] for r in rows]
    plt.figure(figsize=(12, 6))
    plt.bar(bowlers, economy, color="forestgreen")
    plt.title("Top 10 Economical Bowlers in IPL 2015", fontweight="bold")
    plt.xlabel("Bowler")
    plt.ylabel("Economy Rate")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "8_top_10_economical_bowlers_2015.png")
    plt.close()
    print("✓ Saved outputs/8_top_10_economical_bowlers_2015.png")

    conn.close()
    print("Plot generation complete!")


if __name__ == "__main__":
    generate_plots()
