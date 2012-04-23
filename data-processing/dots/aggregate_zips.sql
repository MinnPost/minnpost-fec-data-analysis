DROP TABLE IF EXISTS "public"."fec_amount_by_zip";
CREATE TABLE "public"."fec_amount_by_zip" (
	"zip" varchar(16) NOT NULL,
	"the_geom" "public"."geometry",
	"obama_total" float8,
	"obama_cid" varchar(128),
	"obama_name" varchar(128),
	"romney_total" float8,
	"romney_cid" varchar(128),
	"romney_name" varchar(128),
	"santorum_total" float8,
	"santorum_cid" varchar(128),
	"santorum_name" varchar(128),
	"gingrich_total" float8,
	"gingrich_cid" varchar(128),
	"gingrich_name" varchar(128),
	"paul_total" float8,
	"paul_cid" varchar(128),
	"paul_name" varchar(128),
	PRIMARY KEY ("zip")
)
WITH (OIDS=FALSE);

INSERT INTO "fec_amount_by_zip"
SELECT
	zip."name" AS zip,
	zip."the_geom",
	obama."total" AS obama_total,
	obama."CommID" AS obama_cid,
	obama."name" AS obama_name,
	romney."total" AS romney_total,
	romney."CommID" AS romney_cid,
	romney."name" AS romney_name,
	santorum."total" AS santorum_total,
	santorum."CommID" AS santorum_cid,
	santorum."name" AS santorum_name,
	gingrich."total" AS gingrich_total,
	gingrich."CommID" AS gingrich_cid,
	gingrich."name" AS gingrich_name,
	paul."total" AS paul_total,
	paul."CommID" AS paul_cid,
	paul."name" AS paul_name

FROM
	-- Zips grouped
	(SELECT "name", ST_Union("the_geom") AS the_geom FROM "mn_zip" GROUP BY "name") AS zip
	-- Obama
	LEFT JOIN (SELECT SUM(CAST(s."ContAmount" AS FLOAT)) AS total, SUBSTRING(s."ContZip", 1, 5) as zip, s."CommID", c."short_name" AS name
		FROM "ScheduleAImport" AS s JOIN "committees" AS c ON s."CommID" = c."committee_id"
		WHERE CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
		AND CAST(s."strContDate" AS DATE) < CAST('2012-04-01' AS DATE)
		AND s."ContState" = 'MN' AND s."CommID" = 'C00431445'
		GROUP BY SUBSTRING(s."ContZip", 1, 5), s."CommID", c."short_name") as obama
		ON zip."name" = obama."zip"
	-- Romney
	LEFT JOIN (SELECT SUM(CAST(s."ContAmount" AS FLOAT)) AS total, SUBSTRING(s."ContZip", 1, 5) as zip, s."CommID", c."short_name" AS name
		FROM "ScheduleAImport" AS s JOIN "committees" AS c ON s."CommID" = c."committee_id"
		WHERE CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
		AND CAST(s."strContDate" AS DATE) < CAST('2012-04-01' AS DATE)
		AND s."ContState" = 'MN' AND s."CommID" = 'C00431171'
		GROUP BY SUBSTRING(s."ContZip", 1, 5), s."CommID", c."short_name") as romney
		ON zip."name" = romney."zip"
	-- Santorum
	LEFT JOIN (SELECT SUM(CAST(s."ContAmount" AS FLOAT)) AS total, SUBSTRING(s."ContZip", 1, 5) as zip, s."CommID", c."short_name" AS name
		FROM "ScheduleAImport" AS s JOIN "committees" AS c ON s."CommID" = c."committee_id"
		WHERE CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
		AND CAST(s."strContDate" AS DATE) < CAST('2012-04-01' AS DATE)
		AND s."ContState" = 'MN' AND s."CommID" = 'C00496034'
		GROUP BY SUBSTRING(s."ContZip", 1, 5), s."CommID", c."short_name") as santorum
		ON zip."name" = santorum."zip"
	-- Gingrich
	LEFT JOIN (SELECT SUM(CAST(s."ContAmount" AS FLOAT)) AS total, SUBSTRING(s."ContZip", 1, 5) as zip, s."CommID", c."short_name" AS name
		FROM "ScheduleAImport" AS s JOIN "committees" AS c ON s."CommID" = c."committee_id"
		WHERE CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
		AND CAST(s."strContDate" AS DATE) < CAST('2012-04-01' AS DATE)
		AND s."ContState" = 'MN' AND s."CommID" = 'C00496497'
		GROUP BY SUBSTRING(s."ContZip", 1, 5), s."CommID", c."short_name") as gingrich
		ON zip."name" = gingrich."zip"
	-- Paul
	LEFT JOIN (SELECT SUM(CAST(s."ContAmount" AS FLOAT)) AS total, SUBSTRING(s."ContZip", 1, 5) as zip, s."CommID", c."short_name" AS name
		FROM "ScheduleAImport" AS s JOIN "committees" AS c ON s."CommID" = c."committee_id"
		WHERE CAST(s."strContDate" AS DATE) >= CAST('2012-01-01' AS DATE)
		AND CAST(s."strContDate" AS DATE) < CAST('2012-04-01' AS DATE)
		AND s."ContState" = 'MN' AND s."CommID" = 'C00495820'
		GROUP BY SUBSTRING(s."ContZip", 1, 5), s."CommID", c."short_name") as paul
		ON zip."name" = paul."zip"

ORDER BY
	zip."name"
;