"""Main entry point for IPL SQL Analytics Project.

Executes SQL queries from the queries/ directory against SQLite ipl.db.
"""

import sqlite3
import sys
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db" / "ipl.db"
QUERIES_DIR = BASE_DIR / "queries"
OUTPUTS_DIR = BASE_DIR / "outputs"


def ensure_db_exists():
    """Ensure ipl.db exists, otherwise trigger load_data.py."""
    if not DB_FILE.exists():
        print(f"Database {DB_FILE.name} not found. Ingesting CSV datasets...")
        from db.load_data import load_database
        load_database()


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    ensure_db_exists()
    return sqlite3.connect(DB_FILE)


def print_table(headers: list[str], rows: list[tuple], max_rows: int = None) -> None:
    """Print query results in a clean formatted ASCII table."""
    if not rows:
        print("No results returned.\n")
        return

    display_rows = rows[:max_rows] if max_rows else rows

    # Convert all cell values to string
    str_rows = [[str(cell) if cell is not None else "NULL" for cell in row] for row in display_rows]
    col_widths = [len(h) for h in headers]

    for row in str_rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(separator)
    print(header_line)
    print(separator)
    for row in str_rows:
        print("| " + " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(row)) + " |")
    print(separator)

    if max_rows and len(rows) > max_rows:
        print(f"(Showing first {max_rows} of {len(rows)} rows)\n")
    else:
        print(f"Total rows: {len(rows)}\n")


def execute_sql_file(filename: str, title: str, max_display: int = None) -> list[tuple]:
    """Execute a .sql file from the queries directory and display results."""
    query_path = QUERIES_DIR / filename
    if not query_path.exists():
        print(f"Error: Query file {filename} not found.")
        return []

    sql = query_path.read_text(encoding="utf-8")

    print("\n" + "=" * 65)
    print(f" {title.upper()} ".center(65, "="))
    print("=" * 65)
    print(f"[SQL Query: queries/{filename}]")
    print("-" * 65)
    print(sql.strip())
    print("-" * 65)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        headers = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

    print_table(headers, rows, max_rows=max_display)
    return rows


class IPLSqlDashboard:
    """Interactive CLI Dashboard executing SQL analytics."""

    def show_menu(self) -> None:
        """Display dashboard menu options."""
        print()
        print("=" * 55)
        print("  IPL SQL ANALYTICS DASHBOARD (2008 - 2017)  ".center(55, "="))
        print("=" * 55)
        print("   0) Enter 0 to EXIT")
        print("   1) Total runs scored by each team")
        print("   2) Top 10 RCB batsmen by total runs")
        print("   3) Distinct Foreign Umpires by Country")
        print("   4) Matches played by team per season")
        print("   5) Number of matches played per year")
        print("   6) Number of matches won by each team per year")
        print("   7) Extra runs conceded per team in 2016")
        print("   8) Top 10 economical bowlers in 2015")
        print("   9) Run ALL programs")
        print("=" * 55)

    def program_1(self):
        execute_sql_file("1_total_runs_by_team.sql", "1. Total Runs Scored by Each Team")

    def program_2(self):
        execute_sql_file("2_top_10_rcb_batsmen.sql", "2. Top 10 RCB Batsmen by Total Runs")

    def program_3(self):
        execute_sql_file("3_foreign_umpire_analysis.sql", "3. Foreign Umpires by Country")

    def program_4(self):
        execute_sql_file("4_matches_played_by_team_by_season.sql", "4. Matches Played by Team per Season", max_display=30)

    def program_5(self):
        execute_sql_file("5_matches_played_per_year.sql", "5. Number of Matches Played per Year")

    def program_6(self):
        execute_sql_file("6_matches_won_by_team_per_year.sql", "6. Matches Won by Each Team per Year", max_display=30)

    def program_7(self):
        execute_sql_file("7_extra_runs_conceded_2016.sql", "7. Extra Runs Conceded per Team in 2016")

    def program_8(self):
        execute_sql_file("8_top_10_economical_bowlers_2015.sql", "8. Top 10 Economical Bowlers in 2015")

    def run_all(self):
        self.program_1()
        self.program_2()
        self.program_3()
        self.program_4()
        self.program_5()
        self.program_6()
        self.program_7()
        self.program_8()

    def run(self):
        """Run interactive CLI loop."""
        ensure_db_exists()

        while True:
            self.show_menu()
            try:
                choice = input("Enter your choice [0-9]: ").strip()
                if not choice:
                    continue
                option = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 9.")
                continue

            match option:
                case 0:
                    print("Exiting IPL SQL Analytics. Goodbye!")
                    break
                case 1:
                    self.program_1()
                case 2:
                    self.program_2()
                case 3:
                    self.program_3()
                case 4:
                    self.program_4()
                case 5:
                    self.program_5()
                case 6:
                    self.program_6()
                case 7:
                    self.program_7()
                case 8:
                    self.program_8()
                case 9:
                    self.run_all()
                case _:
                    print("Invalid choice. Please select between 0 and 9.")


if __name__ == "__main__":
    dashboard = IPLSqlDashboard()
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("all", "9"):
            dashboard.run_all()
        elif arg.isdigit() and 1 <= int(arg) <= 8:
            getattr(dashboard, f"program_{arg}")()
        else:
            print(f"Unknown argument: {arg}. Usage: python main.py [1-9|all]")
    else:
        dashboard.run()
