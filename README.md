# IPL Dataset Analytics in SQL (2008 – 2017)

An implementation of the IPL (Indian Premier League) data analytics project using **relational database modeling and SQL queries** powered by SQLite.

---

## 📁 Directory Structure

```
IPL-sql/
├── app/
│   ├── main.py                     # Interactive CLI dashboard & SQL runner
│   └── plot_results.py             # Optional Matplotlib chart generator
├── data/
│   ├── deliveries.csv              # Ball-by-ball IPL dataset (~150k deliveries)
│   ├── matches.csv                 # Match-level dataset (2008–2017, 636 matches)
│   └── umpires.csv                 # Reference dataset mapping umpires to country
├── db/
│   ├── schema.sql                  # DDL defining tables and analytical indexes
│   ├── load_data.py                # Ingestion script to build SQLite ipl.db from CSVs
│   └── ipl.db                      # SQLite relational database
├── queries/                        # Pure SQL queries for each problem
│   ├── 1_total_runs_by_team.sql
│   ├── 2_top_10_rcb_batsmen.sql
│   ├── 3_foreign_umpire_analysis.sql
│   ├── 4_matches_played_by_team_by_season.sql
│   ├── 5_matches_played_per_year.sql
│   ├── 6_matches_won_by_team_per_year.sql
│   ├── 7_extra_runs_conceded_2016.sql
│   └── 8_top_10_economical_bowlers_2015.sql
├── outputs/                        # Generated output charts and exports
├── requirements.txt                # Optional plotting dependencies
└── README.md                       # Documentation
```

---

## 🗄️ Database Schema

The database (`db/ipl.db`) models three tables with indexing on frequently filtered and joined columns:

1. **`matches`**:
   - Primary key: `id`
   - Attributes: `season`, `city`, `date`, `team1`, `team2`, `toss_winner`, `winner`, `win_by_runs`, `win_by_wickets`, `umpire1`, `umpire2`, `umpire3`, etc.
   - Indexes: `idx_matches_season`, `idx_matches_winner`

2. **`deliveries`**:
   - Primary key: `id` (AUTOINCREMENT)
   - Foreign key: `match_id` references `matches(id)`
   - Attributes: `inning`, `batting_team`, `bowling_team`, `over`, `ball`, `batsman`, `bowler`, `batsman_runs`, `extra_runs`, `total_runs`, `bye_runs`, `legbye_runs`, etc.
   - Indexes: `idx_deliveries_match_id`, `idx_deliveries_batting_team`, `idx_deliveries_bowling_team`, `idx_deliveries_batsman`, `idx_deliveries_bowler`

3. **`umpires`**:
   - Primary key: `umpire`
   - Attributes: `country`

---

## 🚀 Getting Started

### 1. Ingest Data into SQLite

Populate `db/ipl.db` from the CSV files:

```bash
python3 db/load_data.py
```

*(Note: If you run `app/main.py` directly, it will automatically build the database if `db/ipl.db` does not exist yet.)*

### 2. Run the Interactive Dashboard

Launch the CLI menu:

```bash
python3 app/main.py
```

You can also run specific queries directly via command-line arguments:

```bash
# Run problem 1
python3 app/main.py 1

# Run all 8 problems
python3 app/main.py all
```

---

## 📊 The 8 Analytical Problems & SQL Queries

### Problem 1: Total Runs Scored by Each Team
**File:** [`queries/1_total_runs_by_team.sql`](queries/1_total_runs_by_team.sql)
```sql
SELECT
    batting_team AS team,
    SUM(total_runs) AS total_runs
FROM deliveries
WHERE batting_team IS NOT NULL AND TRIM(batting_team) != ''
GROUP BY batting_team
ORDER BY total_runs DESC;
```

---

### Problem 2: Top 10 Batsmen for Royal Challengers Bangalore
**File:** [`queries/2_top_10_rcb_batsmen.sql`](queries/2_top_10_rcb_batsmen.sql)
```sql
SELECT
    batsman,
    SUM(batsman_runs) AS total_runs
FROM deliveries
WHERE batting_team = 'Royal Challengers Bangalore'
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;
```

---

### Problem 3: Foreign Umpires by Country
**File:** [`queries/3_foreign_umpire_analysis.sql`](queries/3_foreign_umpire_analysis.sql)
```sql
WITH match_umpires AS (
    SELECT TRIM(umpire1) AS umpire FROM matches WHERE umpire1 IS NOT NULL AND TRIM(umpire1) != ''
    UNION
    SELECT TRIM(umpire2) AS umpire FROM matches WHERE umpire2 IS NOT NULL AND TRIM(umpire2) != ''
    UNION
    SELECT TRIM(umpire3) AS umpire FROM matches WHERE umpire3 IS NOT NULL AND TRIM(umpire3) != ''
)
SELECT
    u.country,
    COUNT(DISTINCT mu.umpire) AS umpire_count
FROM match_umpires mu
JOIN umpires u ON mu.umpire = u.umpire
WHERE u.country != 'India'
GROUP BY u.country
ORDER BY umpire_count DESC, u.country ASC;
```

---

### Problem 4: Matches Played by Team per Season
**File:** [`queries/4_matches_played_by_team_by_season.sql`](queries/4_matches_played_by_team_by_season.sql)
```sql
WITH team_season_matches AS (
    SELECT season, team1 AS team FROM matches
    UNION ALL
    SELECT season, team2 AS team FROM matches
)
SELECT
    season,
    team,
    COUNT(*) AS matches_played
FROM team_season_matches
GROUP BY season, team
ORDER BY season ASC, team ASC;
```

---

### Problem 5: Number of Matches Played per Year
**File:** [`queries/5_matches_played_per_year.sql`](queries/5_matches_played_per_year.sql)
```sql
SELECT
    season AS year,
    COUNT(*) AS total_matches
FROM matches
GROUP BY season
ORDER BY season ASC;
```

---

### Problem 6: Number of Matches Won per Team per Year
**File:** [`queries/6_matches_won_by_team_per_year.sql`](queries/6_matches_won_by_team_per_year.sql)
```sql
SELECT
    season AS year,
    winner AS team,
    COUNT(*) AS matches_won
FROM matches
WHERE winner IS NOT NULL AND TRIM(winner) != ''
GROUP BY season, winner
ORDER BY season ASC, matches_won DESC;
```

---

### Problem 7: Extra Runs Conceded per Team in IPL 2016
**File:** [`queries/7_extra_runs_conceded_2016.sql`](queries/7_extra_runs_conceded_2016.sql)
```sql
SELECT
    d.bowling_team AS team,
    SUM(d.extra_runs) AS extra_runs_conceded
FROM deliveries d
JOIN matches m ON d.match_id = m.id
WHERE m.season = 2016
GROUP BY d.bowling_team
ORDER BY extra_runs_conceded DESC;
```

---

### Problem 8: Top 10 Economical Bowlers in IPL 2015
**File:** [`queries/8_top_10_economical_bowlers_2015.sql`](queries/8_top_10_economical_bowlers_2015.sql)
```sql
SELECT
    d.bowler,
    SUM(d.total_runs - d.bye_runs - d.legbye_runs) AS runs_conceded,
    COUNT(*) AS balls_bowled,
    ROUND(CAST(SUM(d.total_runs - d.bye_runs - d.legbye_runs) AS REAL) * 6.0 / COUNT(*), 2) AS economy_rate
FROM deliveries d
JOIN matches m ON d.match_id = m.id
WHERE m.season = 2015
GROUP BY d.bowler
HAVING balls_bowled > 0
ORDER BY economy_rate ASC
LIMIT 10;
```
