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
5. Create committees table: ```fab committees;```

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
 
### Generate Dot Density Map

Process schedule data to dots and create map.

1. Get requirements, use virtual environment if you want: ```sudo pip install -r data-processing/dots/requirements.txt;```
2. Dot density processing: ```fab dots;```
3. Link Tilemill projects: ```fab tilemill_link;```

## Visualizations

### Q1 Table

To process data for ```q1_top_contributions.html```, do the following:

1. Run ```data-queries/fec_q1_contributions_by_entity.sql```
2. Convert to JSON.  I exported the query results to CSV, then used CSVKit's ```csvjson``` to convert to JSON.
3. Copy JSON into the ```visualizations/q1_top_contributions.html```.

### Q1 Dot Density

1. Render tiles and upload to S3.  Do note that this will take some time.  The final arguments (1,13) are zoom levels and can be changed if needed: ```cd tilemill;  fab map:"fec-q1-dot-density" production export_deploy:32:1:13```
2. Create simplified ZIP geojson dataset.  The transform is needed as the SIMPLIFY function does not handle Lat,Lon (4326) correctly. ```ogr2ogr -f GeoJSON mn_zips.geojson "PG:dbname=minnpost_fec host=localhost user=postgres" -sql "SELECT zip, transform(simplify(transform(the_geom, 2249), 3000), 4326) AS coordinates FROM fec_amount_by_zip"```

## Technologies Used

 - Postgres, PostGIS
 - FEC-Scraper
 - Scraper Wiki
 - TileMill
 - Englewood
 - (many more)
 
## Other Data Sources

 - Zip Code shapefiles from the [US Census Bureau](http://www.census.gov/geo/www/cob/z52000.html), 2000 data.  [Minnesota shapefile](http://www.census.gov/geo/cob/bdy/zt/z500shp/zt27_d00_shp.zip).
 - Zip code max extent: "-97.239209,43.499356,-89.489226,49.384358".