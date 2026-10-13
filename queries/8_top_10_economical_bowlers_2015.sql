-- Problem 8: Top 10 economical bowlers in IPL 2015
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
