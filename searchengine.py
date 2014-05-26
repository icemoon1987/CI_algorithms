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
		
		for i in range(depth):
			newpages = set()

			# Crawl every pages
			for page in pages:

				# Open a page
				try:
					c = urllib2.urlopen(page)
				except:
					print "Could not open %s" % page
					continue

				# Analize and index a page
				soup = BeautifulSoup(c.read())
				self.addtoindex(page, soup)

				links = soup('a')
				for link in links:
					if( 'href' in dict(link.attrs)):
						url = urljoin(page, link['href'])

						if url.find("'") != -1: continue

						url = url.split('#')[0]

						if url[0:4] == 'http' and not self.isindexed(url):
							newpages.add(url)

						linkText = self.gettextonly(link)
						self.addlinkref(page, url, linkText)

				self.dbcommit()

			pages = newpages


	# Create database tables
	def createindextables(self):
		pass




