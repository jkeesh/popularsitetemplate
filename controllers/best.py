import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from datetime import date, datetime, timedelta
import time

import sys
sys.path = ['..'] + sys.path

from datamodel import *
from utils import *


class BestView(webapp.RequestHandler):
	def get(self, siteURL, range):
		now = datetime.now()

		if range == "all":
			delta = None
			besttime = "All Time"
		if range == "month":
			delta = timedelta(weeks=4)
			besttime = "This Month"
		if range == "week":
			delta = timedelta(weeks=1)
			besttime = "This Week"
		if range == "day":
			delta = timedelta(days=1)
			besttime = "Today"
					
		userInfo = getCurrentUserInfo()
		if not userInfo:
			userInfo = createUserInfo()
			
		site = getSiteFromUrl(siteURL)
		if not site:
			self.redirect('/')
	
		siteID = site.key().id()

		items_query = Item.all().order('-upvotes')
		items_query.filter('siteID =', int(siteID))

		limit = None
		if delta:
			limit = now - delta

		#items = items_query.fetch(100)
		items = []
		for item in items_query:
			if limit:
				if item.date >= limit:
					items.append(item)
			else:
				items.append(item)

		
		url = users.create_logout_url(self.request.uri)
		url_linktext = 'logout'
		
		admin = isAdmin(site)
			
		#instead of returning ideas and votes, return a list of 
		#tuples of ideas and votes, this way we can know if the user has voted

		exception = ''
			
		template_values = {
			'items': items,
			'site': site,
			'theUrl': self.request.uri,
			'siteID': siteID,
			'siteName': site.name,
			'url': url,
			'url_linktext': url_linktext,
			'admin': admin,
			'exception': exception,
			'besttime': besttime
		}

		path = os.path.join(os.path.dirname(__file__), '../views/best.html')
		self.response.out.write(template.render(path, template_values))
		
