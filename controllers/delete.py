import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


import sys
sys.path = ['..'] + sys.path

from datamodel import *
from utils import *

class DeleteItem(webapp.RequestHandler):
	def post(self, siteURL, itemID):
		site = getSiteFromUrl(siteURL)
		if not isAdmin(site):
			return
	
		site = getSiteFromUrl(siteURL)
		item = Item.get_by_id(int(itemID))		
		item.delete()
