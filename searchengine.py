# Search engine

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:

	def __init__(self, dbname):
		pass

	def __del__(self):
		pass

	def dbcommit(self):
		pass

	# Get an entry id, if it does not exist, add an entry to database
	def getnetryid(self, table, field, value, createnew=True):
		return None

	# Add index for every web page
	def addtoindex(self, url, soup):
		print "Indexing ", url

	# Get text from a html file
	def gettextonly(self, soup):
		return None

	# Separate words
	def separatewords(self, text):
		return None

	# Return whether the url is indexed
	def isindexed(self, url):
		return False

	# Add the link between two pages into the database
	def addlinkref(self, urlFrom, urlTo, linkText):
		pass

	# Crawl pages
	def crawl(self, pages, depth=2):
		pass

	# Create database tables
	def createindextables(self):
		pass




