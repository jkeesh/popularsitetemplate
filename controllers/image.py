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

class Image(webapp.RequestHandler):
    def get(self):
        item = db.get(self.request.get("img_id"))
        if item.image:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(item.image)
        else:
            self.response.out.write("No image")