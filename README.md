Data analysis of FEC Campaign data.

## Dependencies

We will use a PostGIS database to handle some overhead and store the
data.

1. See [these instructions](https://github.com/MinnPost/minnpost-basemaps/blob/master/README.md) for getting a PostGIS database up and running on a Mac.
2. Create a new PostGIS database called ```minnpost_fec```.  This command should work: ```createdb -U postgres -h localhost -T template_postgis minnpost_fec```

On a Mac, use Brew to get other dependencies.

 - [Install Homebrew](https://github.com/mxcl/homebrew/wiki/installation)
 - ```brew install wget```

## Acquiring Data

Utilizing a 2012-04-17 version of the [FEC Scraper](https://github.com/cschnaars/FEC-Scraper)
we are able to get the data from the FEC.  We are also getting zip data and putting into the DB.

1. We need Fabric: ```sudo pip install fabric;```
2. Basic setup tasks: ```fab setup;```
3. Scrape FEC data; could take some time: ```fab scrape;```
4. Get zips and put in DB: ```fab zips;```
5. Create committees table: ```fab committees```

## Process Data

Now, we will use the FEC Parser to create usable files with this data.  Run the following:

```
fab parse;
```

### Put Data into Postgres

FEC Parse will create tab-delimited text files in the ```~/Data/fec/output``` directory.  These are named with
a time stamp and represent processed files since the last Parse run.

I used Navicat to import these into Postgres.  I am sure there is a way to do this with the command
line, but will have to figure that out first.

Use the following tables names for there respective groups of text files:

 - ScheduleAImport
 
### Generate Dot Density

Process schedule data to dots.

1. Get requirements, use virtual environment if you want: ```sudo pip install -r data-processing/dots/requirements.txt;```
2. Dot density processing: ```fab dots;```

## Visualizations

### Q1 Table

To process data for ```q1_top_contributions.html```, do the following:

1. Run ```data-queries/fec_q1_contributions_by_entity.sql```
2. Convert to JSON.  I exported the query results to CSV, then used CSVKit's ```csvjson``` to convert to JSON.
3. Copy JSON into the ```visualizations/q1_top_contributions.html```.

## Explanation of FEC Data

 - Schedule A: Contributions (Itemized Receipts)
 - Schedule B: Spending (Itemized Disbursements)
 - Schedule C1: ??
 - Schedule C2: ??
 - Schedule D: Debt
 - Schedule E: ??
 - Form 3P Headers: Summary (for monthly??)
 - Cont* = Contributors fields
 
## Committees

### President Candidates

 - C00431445: Obama
 - C00431171: Romney
 - C00495820: Paul
 - C00496497: Gingrich
 - C00496034: Santorum
 
### Minnesota PACs and Parties

 - https://scraperwiki.com/scrapers/fec_mn_2012_pacs_and_parties/

## Technologies Used

 - Postgres, PostGIS
 - FEC-Scraper
 - Scraper Wiki
 
## Other Data Sources

 - Zip Code shapefiles from the [US Census Bureau](http://www.census.gov/geo/www/cob/z52000.html), 2000 data.  [Minnesota shapefile](http://www.census.gov/geo/cob/bdy/zt/z500shp/zt27_d00_shp.zip).  Zip code max extent: "-97.239209,43.499356,-89.489226,49.384358".
 
## Federal Election Commission (FEC) help

 - [Policy on use of data](http://fec.gov/pubrec/publicrecordsoffice.shtml#using)
 - [Vendor tools](http://www.fec.gov/elecfil/vendors.shtml): various tools, including an explanation of forms, schedules, fields, etc.  Relevant file in the ```help``` directory.
 - [Reporting data](http://www.fec.gov/info/report_dates.shtml)
 - Regarding Schedule A, Donor fields used if Entity Types are CCM, PAC or PTY.