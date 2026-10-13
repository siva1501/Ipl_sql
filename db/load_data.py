"""Load CSV datasets into SQLite database."""

import csv
import sqlite3
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "db"
SCHEMA_FILE = DB_DIR / "schema.sql"
DB_FILE = DB_DIR / "ipl.db"


def to_int(val, default=0):
    """Convert value to int safely."""
    if not val:
        return default
    try:
        return int(val.strip())
    except (ValueError, AttributeError):
        return default


def load_database():
    """Create tables and populate them from CSV files."""
    start_time = time.time()
    print("=" * 60)
    print(f"Initializing SQLite database at: {DB_FILE.name}")
    print("=" * 60)

    # Remove existing database file to start fresh
    if DB_FILE.exists():
        DB_FILE.unlink()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Apply schema
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    conn.commit()
    print("✓ Schema initialized successfully.")

    # 1. Load matches.csv
    matches_csv = DATA_DIR / "matches.csv"
    matches_rows = []
    with open(matches_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            matches_rows.append((
                to_int(r["id"]),
                to_int(r["season"]),
                r["city"],
                r["date"],
                r["team1"],
                r["team2"],
                r["toss_winner"],
                r["toss_decision"],
                r["result"],
                to_int(r["dl_applied"]),
                r["winner"],
                to_int(r["win_by_runs"]),
                to_int(r["win_by_wickets"]),
                r["player_of_match"],
                r["venue"],
                r["umpire1"],
                r["umpire2"],
                r["umpire3"],
            ))

    cursor.executemany("""
        INSERT INTO matches (
            id, season, city, date, team1, team2, toss_winner, toss_decision,
            result, dl_applied, winner, win_by_runs, win_by_wickets,
            player_of_match, venue, umpire1, umpire2, umpire3
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, matches_rows)
    conn.commit()
    print(f"✓ Loaded {len(matches_rows):,} rows into 'matches'.")

    # 2. Load umpires.csv
    umpires_csv = DATA_DIR / "umpires.csv"
    umpires_rows = []
    with open(umpires_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("umpire") and r.get("country"):
                umpires_rows.append((r["umpire"].strip(), r["country"].strip()))

    cursor.executemany("""
        INSERT OR REPLACE INTO umpires (umpire, country)
        VALUES (?, ?)
    """, umpires_rows)
    conn.commit()
    print(f"✓ Loaded {len(umpires_rows):,} rows into 'umpires'.")

    # 3. Load deliveries.csv
    deliveries_csv = DATA_DIR / "deliveries.csv"
    print(f"Loading '{deliveries_csv.name}' (this may take a few seconds)...")
    batch_size = 10000
    deliveries_batch = []
    total_deliveries = 0

    with open(deliveries_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            deliveries_batch.append((
                to_int(r["match_id"]),
                to_int(r["inning"]),
                r["batting_team"],
                r["bowling_team"],
                to_int(r["over"]),
                to_int(r["ball"]),
                r["batsman"],
                r["non_striker"],
                r["bowler"],
                to_int(r["is_super_over"]),
                to_int(r["wide_runs"]),
                to_int(r["bye_runs"]),
                to_int(r["legbye_runs"]),
                to_int(r["noball_runs"]),
                to_int(r["penalty_runs"]),
                to_int(r["batsman_runs"]),
                to_int(r["extra_runs"]),
                to_int(r["total_runs"]),
                r["player_dismissed"],
                r["dismissal_kind"],
                r["fielder"],
            ))

            if len(deliveries_batch) >= batch_size:
                cursor.executemany("""
                    INSERT INTO deliveries (
                        match_id, inning, batting_team, bowling_team, over, ball,
                        batsman, non_striker, bowler, is_super_over, wide_runs,
                        bye_runs, legbye_runs, noball_runs, penalty_runs,
                        batsman_runs, extra_runs, total_runs, player_dismissed,
                        dismissal_kind, fielder
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, deliveries_batch)
                total_deliveries += len(deliveries_batch)
                deliveries_batch = []

        if deliveries_batch:
            cursor.executemany("""
                INSERT INTO deliveries (
                    match_id, inning, batting_team, bowling_team, over, ball,
                    batsman, non_striker, bowler, is_super_over, wide_runs,
                    bye_runs, legbye_runs, noball_runs, penalty_runs,
                    batsman_runs, extra_runs, total_runs, player_dismissed,
                    dismissal_kind, fielder
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, deliveries_batch)
            total_deliveries += len(deliveries_batch)

    conn.commit()
    conn.close()

    elapsed = time.time() - start_time
    print(f"✓ Loaded {total_deliveries:,} rows into 'deliveries'.")
    print(f"Database build complete in {elapsed:.2f}s! Stored at {DB_FILE.resolve()}")


if __name__ == "__main__":
    load_database()
