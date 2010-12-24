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

class CommentView(webapp.RequestHandler):
	def post(self, siteURL, itemID):
		item = Item.get_by_id(int(itemID))
		site = getSiteFromUrl(siteURL)
		
		userInfo = getCurrentUserInfo()
		if not userInfo:
			userInfo = createUserInfo()

		comment = Comment()

		#set up comment values
		comment.text = db.Text(self.request.get('content'))
		comment.author = userInfo
		comment.site = site
		comment.item = item
		
		if len(comment.text) == 0:
			self.redirect('/' + siteURL + "/item/" + itemID)
			return
		
		comment.put()
		
		self.redirect('/' + siteURL + "/item/" + itemID)