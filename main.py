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

application = webapp.WSGIApplication(
                                     [('/', MainPage),							#home.py
									  ('/create', CreateSite),					#create.py
									  ('/error/taken', Taken),					#errors.py
									  ('/error/zero', Zero),					#errors.py
									  ('/error/invalid', Invalid),				#errors.py
									  (r'/(.*)/item/(.*)', ItemView),			#itemview.py
									  (r'/(.*)/best/(.*)', BestView),			#best.py
									  (r'/(.*)/newitem', SubmitItem),			#submit.py
									  (r'/(.*)/upvote/(.*)', UpVoteItem),		#votes.py
									  (r'/(.*)/downvote/(.*)', DownVoteItem),	#votes.py
									  (r'/(.*)/comment/(.*)', CommentView),		#comment.py
									  (r'/(.*)/edit(.*)', EditSettings),		#edit.py
									  (r'/(.*)/delete/(.*)', DeleteItem),		#delete.py
									  (r'/img', Image),							#image.py
									  (r'/(.*)', SiteView)],					#siteview.py
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()