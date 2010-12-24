import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from utils import *
from datamodel import *

class CreateSite(webapp.RequestHandler):
	def post(self):
		siteName = self.request.get('siteName')
		siteURL = self.request.get('siteURL').lower()
		siteURL = ''.join(siteURL.split())
		#turn url to lowercase and remove spaces
		
		
		if len(siteName) == 0 or len(siteURL) == 0:
			self.redirect('/error/zero')
			return
			
		if not siteURL.isalnum():
			self.redirect('/error/invalid')
			return
			
		reserved = ['error', 'yoursiteurl', 'img', 'create']
		if siteURL in reserved:
			self.redirect('/error/taken')
			return
			
		alreadyExists = getSiteFromUrl(siteURL)
		self.response.out.write(alreadyExists)
		if alreadyExists != None and  alreadyExists.url:
			self.redirect('/error/taken')
			return
		
		currentUserInfo = getCurrentUserInfo()
		
		if not currentUserInfo:
			currentUserInfo = UserInfo()
			currentUserInfo.user = users.get_current_user()
			currentUserInfo.displayName = users.get_current_user().nickname()
			currentUserInfo.put()
		
		newSite = Site()
		newSite.name = siteName
		newSite.url = siteURL
		newSite.creator = currentUserInfo
		newSite.slogan = ''
		newSite.hasComments = True
		newSite.isAnonymous = False
		newSite.hasPhotos = False
		newSite.upvoteTitle = "Like"
		newSite.downvoteTitle = "Dislike"
		newSite.backgroundColor = "#cccccc"
		newSite.put()
		
		# add the Site to the UserInfo
		currentUserInfo.siteIDs.append(newSite.key().id())
		currentUserInfo.put()
		
		self.redirect(getSiteUrl(newSite))