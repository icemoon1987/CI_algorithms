# Download search engine test pages from http://segaran.com/wiki/

from bs4 import BeautifulSoup

import httplib
import urllib2
import re
import math
import os
import platform
import time


def openUrl(url, repeat = 5):
	print ""
	print "Opening Url: ", url

	page = False

	for i in range(repeat):

		if page != False:
			break;

		try:
			page = urllib2.urlopen(url).read()
		except (IOError, httplib.HTTPException):
			print "Failed ", i+1 , " times!"
			page =  False
			time.sleep(0.5)

	return page

baseUrl = "http://segaran.com/wiki/"
storePath = "./wiki/"

# Create store directory
if not os.path.exists(storePath):
	os.mkdir(storePath)
else:
	print "Already has ", storePath

# Open and store index.html
page = openUrl(baseUrl)
f = open(storePath+"index.html", 'w')
f.write(page)
f.close

# Find all urls
soup = BeautifulSoup(page, "html5lib")

urls = soup.find_all('a')


# Open and store every urls
for link in urls:

	linkname = link['href']

	if -1 == linkname.find("html"):
		continue

	if os.path.exists(storePath+linkname):
		print "Already has ", storePath+linkname
		continue

	print "Downloading ", baseUrl+linkname, " ..."
	page = openUrl(baseUrl+linkname)
	f = open(storePath+linkname, 'w')
	f.write(page)
	f.close



