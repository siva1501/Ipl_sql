-- Problem 3: Foreign umpires by country
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
