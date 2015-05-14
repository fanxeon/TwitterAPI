import web
import time
import tweepy
import json
import couchdb
import datetime
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

# Templates
render = web.template.render('templates/')

# Url configure
urls = (
        "/","index",
        #Twitter related function
        "/twitter", "index",
        "/twitter/(.*)", "getTwitter",
        "/all/(.*)","getAll",
        #User related function
        "/user" , "index",
        "/user/(.*)" , "user"
        )

# Database configure
couch = couchdb.Server()
db = couch['twitter']
usrDb = couch['twitter_users']

# Map function
def fun(doc):
    if doc['date']:
        yield doc['date'], doc

docs = '''function(doc) {
    emit(doc._id, null);
}'''

usernames = '''function(doc) {
    if (doc.user) {
        emit(doc.user.screen_name, null);
    }
}'''


# Main classes
class index:
    def GET(self):
        #i = web.input(name=None)

        #template = "$def with (name)\nHello $name"
        #hello = web.template.Template(template)

        return render.index()

# Get Twitter by ID
class getTwitter:
    def GET(self,docid):
        results = db[docid]
        return render.result(results)

# Twitter - developing
class Twitter:
    def GET(self):
        return None

# Get all twitter - developing
class getAll:
    def GET(self):
        for row in db.query(map_fun):
            counter = counter + 1
            if counter < 10 : # test for display 10 results
                print(row.key)

# User related - developing
class getUser:
    def GET(self):
        return None


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

