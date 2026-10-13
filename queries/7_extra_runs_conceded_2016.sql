-- Problem 7: Extra runs conceded per team in IPL 2016
SELECT
    d.bowling_team AS team,
    SUM(d.extra_runs) AS extra_runs_conceded
FROM deliveries d
JOIN matches m ON d.match_id = m.id
WHERE m.season = 2016
GROUP BY d.bowling_team
ORDER BY extra_runs_conceded DESC;
