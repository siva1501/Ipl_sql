-- Problem 4: Matches played by team per season
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
