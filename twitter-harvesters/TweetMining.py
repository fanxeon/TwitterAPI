import time
import tweepy
import json
import os
import couchdb
import datetime
import random
from textblob import TextBlob

##Environment Variables
#Initial variables
HARVEST_MODE = os.environ['TWITTER_HARVEST_MODE']   # Harvest mode: ('CITY', 'USERS')
logsfile = os.environ['TWITTER_LOGFILE'] #TweetMining.txt'
geoCodeCoordinates = os.environ['TWITTER_GEOCOORD'] #'42.31,-71.05,300km'
geoCityName = os.environ['TWITTER_GEOCITY'] #'Boston'
#Twitter credentials, keep private
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

#Opening output file then printing time log
mylogsfile = open(logsfile, 'a')
mylogsfile.write('Job started on %s.\n' % (datetime.datetime.now()))
mylogsfile.close()


#Twitter API Authentication
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
       #create the users view
    try:
       myusernames = '''function(doc) {
          if (doc.user) {
             emit(doc.user.screen_name, 1);
          }
       }'''
       myreduce ="_count"
       design = { 'views': {
             'usernames': {
                'map': myusernames,
		'reduce': myreduce
              }
        } }

       dbt["_design/tweeters"] = design
    except:
       pass
    myusers = dbt.view('_design/tweeters/_view/usernames', group=True)
    random.shuffle(myusers.rows)  #randomize the users
    for row in myusers:
      get_user_tweets(row.key)
      time.sleep(20) #300 calls limit per 15-min window
   else:
        raise Exception('Invalid HARVEST_MODE {}'.format(HARVEST_MODE))
