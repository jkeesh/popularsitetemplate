# The data model for the popular site website

from google.appengine.ext import db

class UserInfo(db.Model):
	user = db.UserProperty()
	displayName = db.StringProperty()
	siteIDs = db.ListProperty(long) # ids of the Sites that they have created

class Site(db.Model):
	url = db.StringProperty()
	name = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	creator = db.ReferenceProperty(UserInfo)
	slogan = db.StringProperty()
	upvoteTitle = db.StringProperty()
	downvoteTitle = db.StringProperty()
	most_liked_title = db.StringProperty()
	hasComments = db.BooleanProperty()
	hasImages = db.BooleanProperty()
	isAnonymous = db.BooleanProperty()
	hasPhotos = db.BooleanProperty()

class Item(db.Model):
	upvotes = db.IntegerProperty()
	downvotes = db.IntegerProperty()
	content = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.ReferenceProperty(UserInfo)
	site = db.ReferenceProperty(Site)
	siteID = db.IntegerProperty()
	hasImage = db.BooleanProperty()
	image = db.BlobProperty()
	
class Vote(db.Model):
	item = db.ReferenceProperty(Item)
	date = db.DateTimeProperty(auto_now_add=True)
	userInfo = db.ReferenceProperty(UserInfo)
	theVote = db.IntegerProperty() # +1 (upvote), -1 (downvote), 0 (novote)
	
class Comment(db.Model):
	text = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.ReferenceProperty(UserInfo)
	site = db.ReferenceProperty(Site)
	item = db.ReferenceProperty(Item)