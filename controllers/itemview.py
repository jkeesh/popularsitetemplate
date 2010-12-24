import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from utils import *
from datamodel import *

class ItemView(webapp.RequestHandler):
	def get(self, siteURL, itemID):
		userInfo = getCurrentUserInfo()
		if not userInfo:
			userInfo = createUserInfo()
			
		url = users.create_logout_url(self.request.uri)
		url_linktext = 'logout'
		
		site = getSiteFromUrl(siteURL)
		siteID = site.key().id()
		item = Item.get_by_id(int(itemID))	
		
		if not item:
			self.redirect("/"+siteURL)
			
		comments_query = Comment.all().order('date').filter('item =', item)
		comments = comments_query.fetch(100)

		template_values = {
			'comments': comments,
			'item': item,
			'site': site,
			'theUrl': self.request.uri,
			'siteID': siteID,
			'url': url,
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), '../views/item.html')
		self.response.out.write(template.render(path, template_values))