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


def voteFor(item, voteType):
	if not item:
		return
		
	if voteType == 1:
		item.upvotes = item.upvotes + 1
	if voteType == -1:
		item.downvotes = item.downvotes + 1
	item.put()


class UpVoteItem(webapp.RequestHandler):
    def post(self, siteURL, itemID):
		item = Item.get_by_id(int(itemID))		
		voteFor(item, 1)

class DownVoteItem(webapp.RequestHandler):
    def post(self, siteURL, itemID):
		item = Item.get_by_id(int(itemID))		
		voteFor(item, -1)




