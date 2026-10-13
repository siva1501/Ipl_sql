-- Problem 1: Total runs scored by each team in IPL
SELECT
    batting_team AS team,
    SUM(total_runs) AS total_runs
FROM deliveries
WHERE batting_team IS NOT NULL AND TRIM(batting_team) != ''
GROUP BY batting_team
ORDER BY total_runs DESC;

