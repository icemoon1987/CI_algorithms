# Download search engine test pages from http://segaran.com/wiki/

from bs4 import BeautifulSoup

import httplib
import urllib2
import re
import math
import os
import platform
import time

baseUrl = "http://segaran.com/wiki/"

def openUrl(self, url, repeat = 5):
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

page = openUrl(baseUrl)

soup = BeautifulSoup(page, "html5lib")




