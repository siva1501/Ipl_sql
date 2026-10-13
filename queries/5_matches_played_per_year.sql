-- Problem 5: Number of matches played per year in IPL
SELECT
    season AS year,
    COUNT(*) AS total_matches
FROM matches
GROUP BY season
ORDER BY season ASC;
