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

class EditSettings(webapp.RequestHandler):
	def get(self, siteURL, saved):
		displaySaved = False
		if saved: 
			displaySaved = True
			
		site = getSiteFromUrl(siteURL)
		if not isAdmin(site):
			self.redirect('/'+siteURL)
		
		
		url = users.create_logout_url(self.request.uri)
		url_linktext = 'logout'
		
		template_values = {			
			'url': url,
			'url_linktext': url_linktext,
			'site': site,
			'saved': displaySaved
		}
		
		path = os.path.join(os.path.dirname(__file__), '../views/edit.html')
		self.response.out.write(template.render(path, template_values))
	
	def post(self, siteURL, saved):
		
		site = getSiteFromUrl(siteURL)
		
		site.slogan = self.request.get('slogan')
		site.upvoteTitle = self.request.get('upvoteTitle')
		site.downvoteTitle = self.request.get('downvoteTitle')
		site.backgroundColor = self.request.get('color')
		
		comments = self.request.get('comments')
		if comments == "yes":
			site.hasComments = True
		else:
			site.hasComments = False
		
		anon = self.request.get('anon')
		if anon == "yes":
			site.isAnonymous = True
		else:
			site.isAnonymous = False
			
		images = self.request.get('images')
		if images == "yes":
			site.hasPhotos = True
		else:
			site.hasPhotos = False

		site.put()
		self.redirect('/'+siteURL+'/edit/saved')

