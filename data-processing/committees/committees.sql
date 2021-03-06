-- ----------------------------
--  Table structure for "committees"
-- ----------------------------
DROP TABLE IF EXISTS "committees";
CREATE TABLE "committees" (
	"committee_id" varchar(32) NOT NULL,
	"full_name" varchar(512) NOT NULL,
	"candidate_name" varchar(512) NOT NULL,
	"short_name" varchar(512) NOT NULL,
	PRIMARY KEY ("committees")
)
WITH (OIDS=FALSE);

-- ----------------------------
--  Records of "committees"
-- ----------------------------
BEGIN;
INSERT INTO "committees" VALUES ('C00431171', 'Romney for President Inc.', 'Mitt Romney', 'Romney');
INSERT INTO "committees" VALUES ('C00431445', 'Obama for America', 'Barack Obama', 'Obama');
INSERT INTO "committees" VALUES ('C00495820', 'Ron Paul 2012 President Campaign Committee Inc.', 'Ron Paul', 'Paul');
INSERT INTO "committees" VALUES ('C00496497', 'Newt 2012', 'Newt Gingrich', 'Gingrich');
INSERT INTO "committees" VALUES ('C00496034', 'Rick Santorum for President Inc.', 'Rick Santorum', 'Santorum');
COMMIT;


