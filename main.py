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

def getRedirectUrl(listID):
	return '/list/' + str(listID)
	

def getRecentSites():
		sites_query = Site.all().order('-date')
		sites = sites_query.fetch(100)
		return sites

class MainPage(webapp.RequestHandler):
	exception = None #"Error"
	
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'logout'
			
			info = getCurrentUserInfo()
		
			if not info:
				info = UserInfo()
				info.user = users.get_current_user()
				info.displayName = users.get_current_user().nickname()
				info.put()
				
			greeting = info.displayName
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'login'
			greeting = ""


		
		recentSites = getRecentSites()
				
		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'greeting': greeting,
			'recentSites': recentSites,
			'exception': self.exception,
		}

		path = os.path.join(os.path.dirname(__file__), 'views/index.html')
		self.response.out.write(template.render(path, template_values))
		
class Taken(MainPage):
	exception = "Sorry, this url is already taken."
			
class Zero(MainPage):
	exception = "One of the values you entered was empty."
	
class Invalid(MainPage):
	exception = "Your URL contains invalid characters."

application = webapp.WSGIApplication(
                                     [('/', MainPage),
									  ('/create', CreateSite),
									  ('/error/taken', Taken),
									  ('/error/zero', Zero),
									  ('/error/invalid', Invalid),
									  (r'/(.*)/item/(.*)', ItemView),
									  (r'/(.*)/best/(.*)', BestView),
									  (r'/(.*)/newitem', SubmitItem),
									  (r'/(.*)/upvote/(.*)', UpVoteItem),
									  (r'/(.*)/downvote/(.*)', DownVoteItem),
									  (r'/(.*)/comment/(.*)', CommentView),
									  (r'/(.*)/edit(.*)', EditSettings),
									  (r'/(.*)/delete/(.*)', DeleteItem),
									  (r'/img', Image),
									  (r'/(.*)', SiteView)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()