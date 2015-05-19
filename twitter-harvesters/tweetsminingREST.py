import time
import tweepy
import json
import os
import couchdb
import datetime
from textblob import TextBlob

##Environment Variables
#Initial variables
HARVEST_MODE = os.environ['HARVEST_MODE']   # Harvest mode: ('CITY', 'USERS')
logsfile = 'tweetsmininglogsREST.txt'
geoCodeCoordinates = '42.31,-71.05,300km'
geoCityName = 'Boston'
#Twitter credentials, keep private
CONSUMER_KEY = 'VMAXFU1xfYWo8fXeCZlG8FlLq' 
CONSUMER_SECRET = 'GBUtcNEGtxY8qTkd6jErKI70PBAdIDdUyWZwXg1H6QE7KtbKV4'
ACCESS_TOKEN = '3180647443-XiL3H0Yxt3qPq7J2HgyzQGLsBhK7CWAnj3etVgW'
ACCESS_TOKEN_SECRET = 'uD1J2MH7RvQ4MRLrYDlSAc999wHnI8jsPmeK5WHBLG0ky'

#Opening output file then printing time log
mylogsfile = open(logsfile, 'a')
mylogsfile.write('Job started on %s.\n' % (datetime.datetime.now()))
mylogsfile.close()



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, parser=tweepy.parsers.JSONParser())


#twitter db on couchdb
server = couchdb.Server()
try:
    dbt = server.create('twitter')
except:
    dbt = server['twitter']
try:
    dbu = server.create('twitter_users')
except:
    dbu = server['twitter_users']

#TextBlob function to calculate sentiments
def analyse_text(tweet_text):
   tweetanalysis = TextBlob(tweet_text)
   if tweetanalysis.sentiment.polarity < 0:
      sentiment = "negative"
   elif tweetanalysis.sentiment.polarity == 0:
      sentiment = "neutral"
   else:
      sentiment = "positive"
   return({"polarity": tweetanalysis.sentiment.polarity,"subjectivity": tweetanalysis.sentiment.subjectivity,"sentiment": sentiment})

def get_user_tweets(screen_name):
   tweetsPerQry = 100  # this is the max the API permits
   myno = 0
   max_id = 0
   new_tweets = [0],[1]
   try:
    while len(new_tweets) > 0:
      if (max_id <= 0):
         new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry)
      else:
          new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry, max_id=str(max_id))
      for tweetDoc in new_tweets:
            tweetDoc["_id"] = tweetDoc["id_str"]
            max_id = int(float(tweetDoc["_id"])) - 1
            mysentiment = analyse_text(tweetDoc["text"])
            tweetDoc["analytics"] = mysentiment
            dbdoc = dbu.save(tweetDoc)
            myno += 1
      return    #Goes 100 back but can remove to get more!
   except:
      pass  #pass duplication occurence

docs = '''function(doc) {
        emit(doc._id, 1);
}'''

usernames = '''function(doc) {
     if (doc.user) {
        emit(doc.user.screen_name, 1);
     }
}'''

def get_location_tweets(geoCodeCoordinates):
  maxTweets = 44000 #450 calls limit per 15-min window (using 440 as a pre-caution)
  tweetsPerQry = 100  # this is the max the API permits
  tweetCount = 0
  myno = 0
  max_id = 0
  while tweetCount < maxTweets:
      if (max_id <= 0):
         new_tweets = api.search(geocode=geoCodeCoordinates, count=tweetsPerQry)
      else:
         new_tweets = api.search(geocode=geoCodeCoordinates, count=tweetsPerQry, max_id=str(max_id))
      if len(new_tweets["statuses"]) > 0: #Stops when no more old tweets
       for tweetDoc in new_tweets["statuses"]:
         try:
            tweetDoc["_id"] = tweetDoc["id_str"]  #handling duplication by using id_str of tweet
            max_id = int(float(tweetDoc["_id"])) - 1
            if tweetDoc["place"]["name"] == geoCityName:
               mysentiment = analyse_text(tweetDoc["text"])
               tweetDoc["analytics"] = mysentiment  #Add analytics to tweet json
               dbdoc = dbt.save(tweetDoc)
               myno +=1
         except Exception as e:
               pass  #pass duplication occurence

       tweetCount += tweetsPerQry
       if tweetCount == maxTweets:
         maxTweets +=maxTweets #Loop again
         time.sleep(60 * 15) #450 calls limit per 15-min window 

while True:
    
# Harvest City
   if HARVEST_MODE == 'CITY':
        get_location_tweets(geoCodeCoordinates)

#Harvest Users
   elif HARVEST_MODE == 'USERS':
    for row in dbt.view('_design/tweeters/_view/usernames', group=True):
      get_user_tweets(row.key)
      mylogsfile = open(logsfile, 'a')
      mylogsfile.write(row.key)
      mylogsfile.write('User Break %s.\n' % (datetime.datetime.now()))
      mylogsfile.close()
      time.sleep(20) #300 calls limit per 15-min window
   else:
        raise Exception('Invalid HARVEST_MODE {}'.format(HARVEST_MODE))
