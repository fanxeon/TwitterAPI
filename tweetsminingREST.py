import time
import tweepy
import json
import couchdb
import datetime

#logs
logsfile = 'tweetsmininglogs.txt'

#Opening output file then printing time log
mylogsfile = open(logsfile, 'w')
mylogsfile.write('Job started on %s.\n' % (datetime.datetime.now()))

#Twitter credentials, keep private
CONSUMER_KEY = 'VMAXFU1xfYWo8fXeCZlG8FlLq'
CONSUMER_SECRET = 'GBUtcNEGtxY8qTkd6jErKI70PBAdIDdUyWZwXg1H6QE7KtbKV4'
ACCESS_TOKEN = '3180647443-XiL3H0Yxt3qPq7J2HgyzQGLsBhK7CWAnj3etVgW'
ACCESS_TOKEN_SECRET = 'uD1J2MH7RvQ4MRLrYDlSAc999wHnI8jsPmeK5WHBLG0ky'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, parser=tweepy.parsers.JSONParser())

maxTweets = 18000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
sinceId = None
tweetCount = 0
max_id = 0

#twitter db on couchdb
server = couchdb.Server()
try:
    db = server.create('twitter')
except:
    db = server['twitter']

while tweetCount < maxTweets:
      if (max_id <= 0):
         if (not sinceId):
            print('#1')
            new_tweets = api.search(geocode='42.31,-71.05,100km', count=tweetsPerQry, result_type='recent')
         else:
            new_tweets = api.search(geocode='42.31,-71.05,100km', count=tweetsPerQry, since_id=sinceId, result_type='recent')
      else:
         if (not sinceId):
            print('#2')
            new_tweets = api.search(geocode='42.31,-71.05,100km', count=tweetsPerQry, max_id=str(max_id), result_type='recent')
         else:
            new_tweets = api.search(geocode='42.31,-71.05,100km', count=tweetsPerQry, max_id=str(max_id), since_id=sinceId, result_type='recent')
      if not new_tweets:
         print("No more tweets found")
         break

      for tweetDoc in new_tweets["statuses"]:
         try:
#       print(tweetDoc['place'])
            tweetDoc["_id"] = str(tweetDoc["id"])
            if tweetDoc["place"] != "None":
               print(tweetDoc["_id"],tweetDoc["place"]["name"])
               if tweetDoc["place"]["name"] == 'Boston':
                  dbdoc = db.save(tweetDoc)
         except:
            #print(tweetDoc["_id"], "Duplication occured")
            pass

      max_id = int(float(tweetDoc["_id"])) + 1
      tweetCount += tweetsPerQry
      if tweetCount == maxTweets:
         print(max_id)
         print(tweetCount)
         maxTweets +=maxTweets
         time.sleep(60 * 15)
