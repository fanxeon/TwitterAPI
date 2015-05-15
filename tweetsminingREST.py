import time
import tweepy
import json
import couchdb
import datetime
from textblob import TextBlob

#logs
logsfile = 'tweetsmininglogsREST.txt'
geoCodeCoordinates = '42.31,-71.05,300km'
geoCityName = 'Boston'

#Opening output file then printing time log
mylogsfile = open(logsfile, 'a')
mylogsfile.write('Job started on %s.\n' % (datetime.datetime.now()))
mylogsfile.close()

#Twitter credentials, keep private
CONSUMER_KEY = 'VMAXFU1xfYWo8fXeCZlG8FlLq' 
CONSUMER_SECRET = 'GBUtcNEGtxY8qTkd6jErKI70PBAdIDdUyWZwXg1H6QE7KtbKV4'
ACCESS_TOKEN = '3180647443-XiL3H0Yxt3qPq7J2HgyzQGLsBhK7CWAnj3etVgW'
ACCESS_TOKEN_SECRET = 'uD1J2MH7RvQ4MRLrYDlSAc999wHnI8jsPmeK5WHBLG0ky'

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
   print(new_tweets)
   try:
    while len(new_tweets) > 0:
      if (max_id <= 0):
         new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry)
      else:
          new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry, max_id=str(max_id))
      #print(new_tweets[0])
      for tweetDoc in new_tweets:
#       print(tweetDoc['place'])
            tweetDoc["_id"] = tweetDoc["id_str"]
            max_id = int(float(tweetDoc["_id"])) - 1
            print(tweetDoc["_id"])
            mysentiment = analyse_text(tweetDoc["text"])
            tweetDoc["analytics"] = mysentiment
            dbdoc = dbu.save(tweetDoc)
            myno += 1
      return
   except:
      return
   mylogsfile = open(logsfile, 'a')
   mylogsfile.write('max_id: ' + str(max_id) + '\n')
   mylogsfile.write('tweetCount: ' + str(tweetCount) + '\n')
   mylogsfile.write('Step %s.\n' % (datetime.datetime.now()))
   mylogsfile.write('Found: ' + str(myno) + '\n')
   mylogsfile.close()

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
         print('Here:', max_id)
         new_tweets = api.search(geocode=geoCodeCoordinates, count=tweetsPerQry, max_id=str(max_id))
      if len(new_tweets["statuses"]) > 0:
       for tweetDoc in new_tweets["statuses"]:
         try:
            tweetDoc["_id"] = tweetDoc["id_str"]
            max_id = int(float(tweetDoc["_id"])) - 1
#            print(tweetDoc["place"])
#            if tweetDoc["place"] != "None":
            if tweetDoc["place"]["name"] == geoCityName:
               print(tweetDoc["_id"], tweetDoc["place"]["name"])
               mysentiment = analyse_text(tweetDoc["text"])
               tweetDoc["analytics"] = mysentiment

               dbdoc = dbt.save(tweetDoc)
               myno +=1
         except Exception as e:
            if str(e) == "('conflict', 'Document update conflict.')":
               print(tweetDoc["_id"], "Duplication occured")
               return
            else:
               pass

       mylogsfile = open(logsfile, 'a')
       mylogsfile.write('Geo max_id: ' + str(max_id) + '\n')
       mylogsfile.write('Geo tweetCount: ' + str(tweetCount) + '\n')
       mylogsfile.write('Geo Step %s.\n' % (datetime.datetime.now()))
       mylogsfile.write('Geo Found: ' + str(myno) + '\n')
       mylogsfile.close()

       tweetCount += tweetsPerQry
       if tweetCount == maxTweets:
         mylogsfile = open(logsfile, 'a')
         mylogsfile.write('Geo max_id: ' + str(max_id) + '\n')
         mylogsfile.write('Geo tweetCount: ' + str(tweetCount) + '\n')
         mylogsfile.write('Geo Break %s.\n' % (datetime.datetime.now()))
         mylogsfile.write('Geo Found: ' + str(myno) + '\n')
         mylogsfile.close()
         maxTweets +=maxTweets
         time.sleep(60 * 15) #450 calls limit per 15-min window 

while True:
   get_location_tweets(geoCodeCoordinates)

#Users Loop
   for row in dbt.view('_design/tweeters/_view/usernames', group=True):
      get_user_tweets(row.key)
      mylogsfile = open(logsfile, 'a')
      mylogsfile.write(row.key)
      mylogsfile.write('User Break %s.\n' % (datetime.datetime.now()))
      mylogsfile.close()
      time.sleep(20) #300 calls limit per 15-min window
      get_location_tweets(geoCodeCoordinates)
