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
cp data-processing/usersettings.py.example usersettings.py;
```

Now, update ```data-processing/usersettings.py``` with the appropriate location;  It is suggested
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
cd data-processing;
python FECScraper.py;
```

## Process Data

Now, we will use the FEC Parser to create usable files with this data.  Run the following:

```
python FECParser.py;
```

## Technologies Use

 - Postgres, PostGIS
 - FEC-Scraper