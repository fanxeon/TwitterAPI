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

class Tweet (Document) :
    name = TextField()
    text = TextField()
    id_id = TextField()


# Main classes
class index:
    def GET(self):
        #i = web.input(name=None)
        return render.index()

# Get Twitter by ID
class getTwitter:
    def GET(self,docid):
        results = db.get(docid)
        if results['analytics']['sentiment'] == 'positive' :
            return render.result_pos(results)
        elif results['analytics']['sentiment'] == 'negative' :
            return render.result_neg(results)
        else :
            return render.result(results)

# Further functions developing
class Twitter:
    def GET(self):
        return None

# Overview
class getAll:
    def GET(self):
        for row in db.query(map_fun):
            counter = counter + 1
            if counter < 10 : # test for display 10 results
                print(row.key)

# User related
class getUser:
    def GET(self):
        return None

# Def -  function parts
def get_tweets(self):
    return self.db.view('twitter/get_tweets')


# Views
def _create_views(self):
    count_map = 'function(doc) { emit(doc.id, 1); }'
    count_reduce = 'function(keys, values) { return sum(values); }'
    view = couchdb.design.ViewDefinition('twitter', 'count_tweets', count_map, reduce_fun=count_reduce)
    view.sync(self.db)
    
    get_tweets = 'function(doc) { emit(("0000000000000000000"+doc.id).slice(-19), doc); }'
    view = couchdb.design.ViewDefinition('twitter', 'get_tweets', get_tweets)
    view.sync(self.db)


def save_tweet(self, tw):
    tw['_id'] = tw['id_str']
    self.db.save(tw)

def count_tweets(self):
    for doc in self.db.view('twitter/count_tweets'):
        return doc.value

def get_tweets(self):
    return self.db.view('twitter/get_tweets')



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

