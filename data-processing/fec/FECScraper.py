# FEC Scraper
# By Christopher Schnaars and Anthony DeBarros, USA TODAY
# Developed with Python 2.7.2

"""
The purpose of this script is to scrape campaign finance reports
from the Federal Election Commission (FEC) website for a specified
group of committees.

You are strongly encouraged to consult the documentation in README.txt
before using this scraper so you'll understand what it does (and does
not) do. In a nutshell, it captures only Form 3 filings by committees
you specify below.

Optionally, the script can interact with a database to help manage
your downloaded data. Complete details can be found in README.txt.
To do this, make sure the usedatabaseflag user variable is set to 1.

You can specify up to three directories for various files:
 * savedir: This is where scraped files will be saved.
 * reviewdir: This is a directory where you can house files that you have not
imported into your database because the data requires cleanup before it
can be successfully imported. This script uses this directory only to look
for files that previously have been downloaded. No files in this directory
will be altered, and no new files will be saved here.
 * processeddir: Similarly, you can put files you've already imported
into a database in this directory. As with reviewdir, the script will use
this directory only to look for files that previously have been downloaded.
It will not alter files in this directory or save new files here.

You'll find commented code below to show you how to explicitly
download filings for a particular committee.
"""

# User variables

# Try to import your user settings or set them explicitly. The database
# connection string will be ignored if database integration is disabled.
try:
    exec(open('usersettings.py').read())
except:
    maindir = '/Users/USERNAME/Data/fec-scraper/'
    connstr = 'DRIVER={Postgres};SERVER=localhost;DATABASE=minnpost_fec;UID=postgres;PWD=;'
    
# Directories: You can edit these to customize file locations.
savedir = maindir + 'import/'
reviewdir = maindir + 'review/'
processeddir = maindir + 'processed/'

# Set this flag to 1 if you want the script to interact with a database.
# Set it to 0 if the script should run independent of any database.
# A database is used solely to look for committees and files that
# previously have been downloaded.
usedatabaseflag = 0

# Import libraries
import re, urllib, glob, os

# Create lists to hold committee and file IDs
commidlist = []
fileidlist = []

# Display start message
print 'Compiling lists of FEC committees and previously downloaded files...'

# Create database connection to fetch lists of committee IDs and file IDs already in the database
# The code below works with SQL Server; see README for tips on connecting
# to other database managers.
if usedatabaseflag == 1:
    import pyodbc
    conn = pyodbc.connect(connstr)
    cursor = conn.cursor()

    # Execute stored procedure and populate list with committee IDs
    sql = 'EXEC usp_GetCommitteeIDs'
    for row in cursor.execute(sql):
        commidlist += row

    # Execute stored procedure and populate list with file IDs
    sql = 'EXEC usp_GetFileIDs'
    for row in cursor.execute(sql):
        fileidlist += row

    # Close database connection
    conn.close()

# Add IDs for files in review directory
for datafile in glob.glob(os.path.join(reviewdir, '*.fec')):
    fileidlist.append(datafile.replace(reviewdir, '')[:6])

# Add IDs for files in save directory
for datafile in glob.glob(os.path.join(savedir, '*.fec')):
    fileidlist.append(datafile.replace(savedir, '')[:6])

# Add IDs for files in processed directory

for datafile in glob.glob(os.path.join(processeddir, '*.fec')):
   fileidlist.append(datafile.replace(processeddir, '')[:6])

# Sort the fileid list
fileidlist.sort()

# If you need to add committee IDs for candidates or PACs for which
# you've never previously downloaded data, you can do that here like this:
try:
    for line in open('commidappend.txt', 'rb'):
        if len(line.strip()) == 9 and line.startswith('C'):
            commidlist.append(line.strip())
except:
    pass
finally:
    # commidlist.append('C00431445') # Obama for America
    # commidlist.append('C00500587') # RickPerry.org Inc.
    # commidlist.append('C00431171') # Romney for President Inc.
    pass

# Begin scrape
print 'Done!\n'
print 'Initializing FEC scrape...'
print 'Fetching data for ' + str(len(commidlist)) + ' committees.\n'

# Set up a list to house all available file IDs
filing_numbers = []

# Set a regular expression to match six-digit numbers
regex = re.compile(r'[0-9]{6}')

# For each committee id, open the page and read its HTML
for x in commidlist:
    print 'Searching files for ' + x + '.'
    url = "http://query.nictusa.com/cgi-bin/dcdev/forms/" + x + "/"
    html = urllib.urlopen(url)
    response = html.read()

    # For each line in the HTML, look for "Form F3" and a six-digit number
    # and build a list
    for line in response.splitlines():
        if re.search("Form F3", line) and re.search(regex, line):
            filing_numbers += re.findall(regex, line)

filing_numbers.sort()

# Create another list for file IDs to download
downloadlist = []

# Compile list of file IDs that have not been downloaded previously
for x in filing_numbers:
    if fileidlist.count(x) == 0:
        downloadlist.append(x)

# File search completed
print '\nFile search completed. Beginning download...\n'

# For each retrieved filing number, download and save the files.
for y in downloadlist:
    filename = y + ".fec"
    print 'Downloading ' + filename + '.'
    url2 = "http://query.nictusa.com/dcdev/posted/" + filename
    urllib.urlretrieve(url2, savedir + filename)

# Display completion message
print 'File download complete!'
