SELECT DISTINCT
	CASE 
		WHEN s."ContOrgName" NOT IN ('', ',') THEN s."ContOrgName"
		ELSE (INITCAP(s."ContLastName") || ', ' || INITCAP(s."ContFirstName"))
		END AS name,
	to_char(SUM(CAST(s."ContAmount" AS FLOAT)), '999G999G999G999D99') AS sum_amount,
	c."candidate_name",
	COUNT(s."TransID") AS Transactions,
	s."EntityType"
FROM 
	"ScheduleAImport" AS s
	JOIN "committees" AS c
		ON s."CommID" = c."committee_id"
WHERE 
 	CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
 	AND CAST(s."strContDate" AS DATE) < CAST('2013-04-01' AS DATE)
 	AND s."ContState" = 'MN'
GROUP BY 
	(s."ContLastName" || ', ' || s."ContFirstName"),
	c."candidate_name",
	s."ContOrgName",
	s."EntityType",
	s."ContLastName",
	s."ContFirstName"
HAVING 
	SUM(CAST(s."ContAmount" AS FLOAT)) > 500
ORDER BY
	sum_amount DESC,
	name
;