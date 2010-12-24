import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from operator import attrgetter

from datamodel import *

def createUserInfo():
	info = UserInfo()
	info.user = users.get_current_user()
	info.displayName = users.get_current_user().nickname()
	info.put()
	return info

def getCurrentUserInfo():
	return db.GqlQuery("SELECT * FROM UserInfo WHERE user = :1", users.get_current_user()).get()

def getSiteUrl(site):
	return '/' + site.url;
	
def getSiteFromUrl(url):
	return db.GqlQuery("SELECT * FROM Site WHERE url = :1", url).get()
	
	
# Gets the Vote on this idea for the current user or returns none if they have not voted	
def getVoteOnIdea(item):
	userInfo = getCurrentUserInfo()
	return db.GqlQuery("SELECT * FROM Vote WHERE userInfo = :1 AND item = :2", userInfo, item).get()
	
	
def isAdmin(site):
	userInfo = getCurrentUserInfo()
	if not userInfo:
		return 0
	if site.creator.key().id() == userInfo.key().id():
		return 1
	return 0


	

