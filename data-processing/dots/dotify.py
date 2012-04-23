#!/usr/bin/env python

"""
Creates a dot density distribution of FEC campaign data (see README.md).

Utilizes the Englewood project.
@see https://github.com/newsapps/englewood
"""

from englewood import DotDensityPlotter 

def get_data(feature):
  """
  This function is called for each feature Englewood processes and needs to return a
  dictionary of classes, with a number assigned to each. Englewood will divide this
  number by a "dots_per" value set below and create that many dots for that class
  within the geography.
  """
  return {
    'obama': feature.GetFieldAsInteger(feature.GetFieldIndex('obama_total')),
    'romney': feature.GetFieldAsInteger(feature.GetFieldIndex('romney_total')),
    'santorum': feature.GetFieldAsInteger(feature.GetFieldIndex('santorum_total')),
    'gingrich': feature.GetFieldAsInteger(feature.GetFieldIndex('gingrich_total')),
    'paul': feature.GetFieldAsInteger(feature.GetFieldIndex('paul_total'))
  }

# From PostGIS, see setup in README.md
source = "PG: host=localhost dbname='minnpost_fec' user='postgres'"
source_layer = 'fec_totals_by_zip'

# Output to new PostGIS table
dest_driver = 'PostgreSQL'
dest = 'PG:dbname=minnpost_fec host=localhost user=postgres'
dest_layer = 'ScheduleAImport_dots'

# Dots
dots_per = 1

# Perform density plotting
dots = DotDensityPlotter(source, source_layer, dest_driver, dest, dest_layer, get_data, dots_per)
dots.plot()