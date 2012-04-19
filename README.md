Data analysis of FEC Campaign data.

## Setup Database

We will use a PostGIS database to handle some overhead and store the
data.

1. See [these instructions](https://github.com/MinnPost/minnpost-basemaps/blob/master/README.md) for getting a PostGIS database up and running on a Mac.
2. Create a new PostGIS database called ```minnpost_fec```.  This command should work: ```createdb -U postgres -h localhost -T template_postgis minnpost_fec```

## Acquiring Data

Utilizing a 2012-04-17 version of the [FEC Scraper](https://github.com/cschnaars/FEC-Scraper)
we are able to get the data from the FEC.

### Setup

We have to create a few places for things to go.  Create the user settings file:

```
cp data-processing/fec/usersettings.py.example data-processing/fec/usersettings.py;
```

Now, update ```data-processing/fec/usersettings.py``` with the appropriate location;  It is suggested
that you use something like this: ```/Users/USERNAME/Data/fec-scraper/``` (trailing slash is important)

Then, finally, make sure that the sub directories exist.

```
mkdir -p ~/Data/fec-scraper/import;
mkdir -p ~/Data/fec-scraper/output; 
mkdir -p ~/Data/fec-scraper/processed; 
mkdir -p ~/Data/fec-scraper/review; 
```

### Scraping

To scrape the data, use the following command.  Please note that this will take
some time as there are many files to download.  The code is assuming that you are 
using the database set up from above.

```
cd data-processing/fec;
python FECScraper.py;
```
 
### Get Zip Outlines

The following will download the relevant shapefile and import it into PostGIS.

```
wget http://www.census.gov/geo/cob/bdy/zt/z500shp/zt27_d00_shp.zip;
unzip zt27_d00_shp.zip -d zt27_d00;
shp2pgsql -c -I -s 4326 zt27_d00/zt27_d00 mn_zip | psql -U postgres -h localhost minnpost_fec;
```

## Process Data

Now, we will use the FEC Parser to create usable files with this data.  Run the following:

```
cd data-processing/fec;
python data-processing/FECParser.py;
```

### Put Data into Postgres

FEC Parse will create tab-delimited text files in the ```output``` directory.  These are named with
a time stamp and represent processed files since the last Parse run.

I used Navicat to import these into Postgres.  I am sure there is a way to do this with the command
line, but will have to figure that out first.

Use the following tables names for there respective groups of text files:

 - ScheduleAImport
 
### Committee Data

Import in committee data.

```
psql -U postgres -h localhost < data-processing/committees/committees.sql;
```

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