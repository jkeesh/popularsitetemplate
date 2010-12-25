from home import *

class Taken(MainPage):
	exception = "Sorry, this url is already taken."

class Zero(MainPage):
	exception = "One of the values you entered was empty."

class Invalid(MainPage):
	exception = "Your URL contains invalid characters."