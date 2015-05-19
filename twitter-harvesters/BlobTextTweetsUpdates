import time
import tweepy
import json
import couchdb
import datetime
from textblob import TextBlob

#twitter db on couchdb
server = couchdb.Server()
try:
    db = server.create('twitter')
except:
    db = server['twitter']
try:
    dbu = server.create('twitter_users')
except:
    dbu = server['twitter_users']


docs = '''function(doc) {
        emit(doc._id, doc.text);
}'''

def updateDoc(id, json):
    doc = db.get(id)
    doc["analytics"] = json
    doc = db.save(doc)

for row in db.query(docs):
         if len(row) > 0:
            tweetanalysis = TextBlob(row.value)
            if tweetanalysis.sentiment.polarity < 0:
               sentiment = "negative"
            elif tweetanalysis.sentiment.polarity == 0:
               sentiment = "neutral"
            else:
               sentiment = "positive"
            mysentiment = {"polarity": tweetanalysis.sentiment.polarity,"subjectivity": tweetanalysis.sentiment.subjectivity,"sentiment": sentiment}
            updateDoc(row.key, mysentiment)
