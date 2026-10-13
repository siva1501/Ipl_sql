-- Problem 2: Top 10 batsmen for Royal Challengers Bangalore
SELECT
    batsman,
    SUM(batsman_runs) AS total_runs
FROM deliveries
WHERE batting_team = 'Royal Challengers Bangalore'
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;
