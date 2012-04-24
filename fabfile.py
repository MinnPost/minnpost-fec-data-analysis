#!/usr/bin/env python
"""
Fab file to help with managing project.  For docs on Fab file, please see: http://docs.fabfile.org/
"""
import sys
import os
import warnings
from fabric.api import *

"""
Base configuration
"""
env.project_name = 'minnpost-fec-data-analysis'
env.pg_host = 'localhost'
env.pg_dbname = 'minnpost_fec'
env.pg_user = 'postgres'
env.pg_pass = ''


"""
Environments
"""
def production():
  """
  Work on production environment
  """
  env.settings = 'production'
  # env.s3_bucket = env.project_name


def staging():
  """
  Work on staging environment
  """
  env.settings = 'staging'
  # env.s3_bucket = 'staging-%(project_name)s' % env


def setup():
  """
  Do basic setup tasks.
  """
  # Make processing directories
  local('mkdir -p ~/Data/fec-scraper/import; mkdir -p ~/Data/fec-scraper/output;')
  local('mkdir -p ~/Data/fec-scraper/processed; mkdir -p ~/Data/fec-scraper/review');
  
  # Check for user settings
  exists = os.path.exists('data-processing/fec/usersettings.py')
  if exists != True:
     local('cp data-processing/fec/usersettings.py.example data-processing/fec/usersettings.py;')


def scrape():
  """
  Run scraper
  """
  local('cd data-processing/fec && python FECScraper.py')


def parse():
  """
  Run parser
  """
  local('cd data-processing/fec && python FECParser.py')


def zips():
  """
  Get zips and put in the DB
  """
  local('wget http://www.census.gov/geo/cob/bdy/zt/z500shp/zt27_d00_shp.zip;')
  local('unzip zt27_d00_shp.zip -d zt27_d00;')
  local(('shp2pgsql -c -I -s 4326 zt27_d00/zt27_d00 mn_zip | psql -U %(pg_user)s -h %(pg_host)s %(pg_dbname)s;') % env)


def committees():
  """
  Get zips and put in the DB
  """
  local(('psql -U %(pg_user)s -h %(pg_host)s %(pg_dbname)s < data-processing/committees/committees.sql;') % env)


def dots():
  """
  Create dot density.
  
  @see https://github.com/newsapps/englewood
  """
  # Drop and create aggregate table, then run the aggregate query.
  local(('psql -U %(pg_user)s -h %(pg_host)s %(pg_dbname)s < data-processing/dots/aggregate_zips.sql;') % env)
  
  # Drop destination table
  local(('psql -U %(pg_user)s -h %(pg_host)s %(pg_dbname)s -c "DROP TABLE IF EXISTS ScheduleAImport_dots";') % env)
  
  # Get dependencies
  from englewood import DotDensityPlotter 

  # Callback for dot density processing
  def get_data(feature):
    return {
      'obama': feature.GetFieldAsInteger(feature.GetFieldIndex('obama_total')),
      'romney': feature.GetFieldAsInteger(feature.GetFieldIndex('romney_total')),
      'santorum': feature.GetFieldAsInteger(feature.GetFieldIndex('santorum_total')),
      'gingrich': feature.GetFieldAsInteger(feature.GetFieldIndex('gingrich_total')),
      'paul': feature.GetFieldAsInteger(feature.GetFieldIndex('paul_total'))
    }

  # From PostGIS, see setup in README.md
  source = 'PG: host=%(pg_host)s dbname=%(pg_dbname)s user=%(pg_user)s' % env
  source_layer = 'fec_amount_by_zip'
  
  # Output to new PostGIS table
  dest_driver = 'PostgreSQL'
  dest = 'PG: host=%(pg_host)s dbname=%(pg_dbname)s user=%(pg_user)s' % env
  dest_layer = 'ScheduleAImport_dots'
  
  # Dots per dollar
  dots_per = 20
  
  # Perform density plotting
  print 'Creating dots...'
  dots = DotDensityPlotter(source, source_layer, dest_driver, dest, dest_layer, get_data, dots_per)
  dots.plot()


"""
Commands - deployment
"""
def deploy():
  """
  Deploy the latest version of the site to the server and restart Apache2.
  
  Does not perform the functions of load_new_data().
  """
  require('settings', provided_by=[production, staging])

  deploy_to_s3()


def deploy_to_s3():
  """
  Deploy the latest project site media to S3.
  """
  local(('s3cmd -P --guess-mime-type sync ./assets/ s3://%(s3_bucket)s/%(project_name)s/') % env)


"""
Deaths, destroyers of worlds
"""
def shiva_the_destroyer():
  """
  Remove all directories, databases, etc. associated with the application.
  """
  with settings(warn_only=True):
    run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s' % env)
    local('rm -rf ~/Data/fec-scraper/import; rm -rf ~/Data/fec-scraper/output;')
    local('rm -rf ~/Data/fec-scraper/processed; rm -rf ~/Data/fec-scraper/review')
    local('rm -f zt27_d00_shp.zip')
    local('rm -rf zt27_d00')