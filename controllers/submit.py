import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from operator import attrgetter

# This imports the datamodel into the namespace
from datamodel import *
from utils import *

class SubmitItem(webapp.RequestHandler):
	def post(self, siteURL):
		item = Item()
		
		userInfo = getCurrentUserInfo()
		if not userInfo:
			userInfo = createUserInfo()

		item.author = userInfo
		item.content = db.Text(self.request.get('content'))
		
		if len(item.content) == 0:
			self.redirect('/' + siteURL)
			return
	
		item.upvotes = 0
		item.downvotes = 0
		
		
		#get site for this url
		site = getSiteFromUrl(siteURL)
		
		if site.hasPhotos:
			image = self.request.get('image')
			if image:
				item.image = db.Blob(image)
				item.hasImage = True
			else:
				item.hasImage = False
		else:
			item.hasImage = False
		
		item.siteID = int(site.key().id())
		item.site = site
		item.put()
		
		
		
		self.redirect('/' + siteURL)
