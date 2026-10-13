-- Schema definition for IPL Dataset Analytics in SQL

DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS umpires;

-- Matches Table
CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    season INTEGER NOT NULL,
    city TEXT,
    date TEXT,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    toss_winner TEXT,
    toss_decision TEXT,
    result TEXT,
    dl_applied INTEGER DEFAULT 0,
    winner TEXT,
    win_by_runs INTEGER DEFAULT 0,
    win_by_wickets INTEGER DEFAULT 0,
    player_of_match TEXT,
    venue TEXT,
    umpire1 TEXT,
    umpire2 TEXT,
    umpire3 TEXT
);

-- Deliveries Table (Ball-by-ball details)
CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    inning INTEGER NOT NULL,
    batting_team TEXT NOT NULL,
    bowling_team TEXT NOT NULL,
    over INTEGER NOT NULL,
    ball INTEGER NOT NULL,
    batsman TEXT NOT NULL,
    non_striker TEXT NOT NULL,
    bowler TEXT NOT NULL,
    is_super_over INTEGER DEFAULT 0,
    wide_runs INTEGER DEFAULT 0,
    bye_runs INTEGER DEFAULT 0,
    legbye_runs INTEGER DEFAULT 0,
    noball_runs INTEGER DEFAULT 0,
    penalty_runs INTEGER DEFAULT 0,
    batsman_runs INTEGER DEFAULT 0,
    extra_runs INTEGER DEFAULT 0,
    total_runs INTEGER DEFAULT 0,
    player_dismissed TEXT,
    dismissal_kind TEXT,
    fielder TEXT,
    FOREIGN KEY (match_id) REFERENCES matches(id)
);

-- Umpires Reference Table
CREATE TABLE umpires (
    umpire TEXT PRIMARY KEY,
    country TEXT NOT NULL
);

-- Indexes for optimized analytical queries
CREATE INDEX IF NOT EXISTS idx_matches_season ON matches(season);
CREATE INDEX IF NOT EXISTS idx_matches_winner ON matches(winner);
CREATE INDEX IF NOT EXISTS idx_deliveries_match_id ON deliveries(match_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_batting_team ON deliveries(batting_team);
CREATE INDEX IF NOT EXISTS idx_deliveries_bowling_team ON deliveries(bowling_team);
CREATE INDEX IF NOT EXISTS idx_deliveries_batsman ON deliveries(batsman);
CREATE INDEX IF NOT EXISTS idx_deliveries_bowler ON deliveries(bowler);
