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
# Other imports for different url handlers
from controllers import *

def getRecentSites():
	sites_query = Site.all().order('-date')
	sites = sites_query.fetch(100)
	return sites

def getPopularSites():
	sites_query = Site.all().order('-views')
	sites = sites_query.fetch(100)
	return sites

class MainPage(webapp.RequestHandler):
	exception = None #"Error"
	
	def get(self):
		userInfo, loggedIn, url = getUserStatus(self)
		recentSites = getRecentSites()
		popularSites = getPopularSites()
		
		template_values = {
			'url': url,
			'userInfo': userInfo,
			'recentSites': recentSites,
			'popularSites': popularSites,
			'exception': self.exception,
			'loggedIn': loggedIn,
		}
	
		path = os.path.join(os.path.dirname(__file__), '../views/index.html')
		self.response.out.write(template.render(path, template_values))