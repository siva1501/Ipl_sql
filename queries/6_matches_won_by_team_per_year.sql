-- Problem 6: Number of matches won per team per year in IPL
SELECT
    season AS year,
    winner AS team,
    COUNT(*) AS matches_won
FROM matches
WHERE winner IS NOT NULL AND TRIM(winner) != ''
GROUP BY season, winner
ORDER BY season ASC, matches_won DESC;
