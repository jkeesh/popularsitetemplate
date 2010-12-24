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


class SiteView(webapp.RequestHandler):
	def get(self, siteURL):

		userInfo = getCurrentUserInfo()
		if not userInfo:
			userInfo = createUserInfo()
			
		theSite = getSiteFromUrl(siteURL)
		if not theSite:
			self.redirect('/')
		
		if not theSite.backgroundColor:
			theSite.backgroundColor = "#ccc"
			theSite.put()
	
		siteID = theSite.key().id()
		
		items_query = Item.all().order('-date')
		items_query.filter('siteID =', int(siteID))
		items = items_query.fetch(100)
		
		url = users.create_logout_url(self.request.uri)
		url_linktext = 'logout'
		
		admin = isAdmin(theSite)
			
		#instead of returning ideas and votes, return a list of 
		#tuples of ideas and votes, this way we can know if the user has voted

		exception = ''
			
		template_values = {
			'items': items,
			'site': theSite,
			'theUrl': self.request.uri,
			'siteID': siteID,
			'siteName': theSite.name,
			'url': url,
			'url_linktext': url_linktext,
			'admin': admin,
			'exception': exception,
		}

		path = os.path.join(os.path.dirname(__file__), '../views/site.html')
		self.response.out.write(template.render(path, template_values))
		
