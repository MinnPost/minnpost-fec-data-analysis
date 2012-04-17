Data analysis of FEC Campaign data.

## Setup Database

We will use a PostGIS database to handle some overhead and store the
data.

1. See [these instructions](https://github.com/MinnPost/minnpost-basemaps/blob/master/README.md) for getting a PostGIS database up and running on a Mac.
2. Create a new PostGIS database called ```minnpost_fec```.  This command should work: ```createdb -U postgres -h localhost -T template_postgis minnpost_fec```

## Requiring Data

Utilizing a 2012-04-17 version of the [FEC Scraper](https://github.com/cschnaars/FEC-Scraper)
we are able to get the data from the FEC.

To scrape the data, use the following command.  Please note that this will take
some time as there are many files to download.  The code is assuming that you are 
using the database set up from above.

```
mkdir -p ~/Data/fec-scraper/import;
mkdir -p ~/Data/fec-scraper/output; 
mkdir -p ~/Data/fec-scraper/processed; 
mkdir -p ~/Data/fec-scraper/review; 
cd data-processing;
python FECScraper.py;
```