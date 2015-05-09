import time
import tweepy
import json
import couchdb
import datetime

#logs
logsfile = '/home/ubuntu/TwitterAPI/tweetsmininglogsREST.txt'
#logsfile = 'tweetsmininglogsREST.txt'

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

maxTweets = 13000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
sinceId = None
tweetCount = 0
myno = 0
max_id = 424275284624699392

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

def get_all_tweets(screen_name):
   tweetsPerQry = 100  # this is the max the API permits
   myno = 0
   max_id = 0
   new_tweets = [0],[1]
#   new_tweets = api.user_timeline(screen_name = screen_name,count=1)
   print(new_tweets)
   while len(new_tweets) > 0:
      if (max_id <= 0):
         new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry)
      else:
          new_tweets = api.user_timeline(screen_name = screen_name,count=tweetsPerQry, max_id=str(max_id))
      #print(new_tweets[0])
      for tweetDoc in new_tweets:
         try:
#       print(tweetDoc['place'])
            tweetDoc["_id"] = tweetDoc["id_str"]
            max_id = int(float(tweetDoc["_id"])) - 1
            print(tweetDoc["_id"])
            dbdoc = dbu.save(tweetDoc)
            myno += 1
         except:
            #print(tweetDoc["_id"], "Duplication occured")
            pass
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

while tweetCount < maxTweets:
#      for row in dbt.query(docs, '_count', descending=True, limit=1, group=True):
#         if len(row) > 0:
#            print(row.key)
#            #max_id = row.key
#         else:
#            max_id = 0

      if (max_id <= 0):
         new_tweets = api.search(geocode='42.31,-71.05,300km', count=tweetsPerQry)
      else:
         print('Here:', max_id)
         new_tweets = api.search(geocode='42.31,-71.05,300km', count=tweetsPerQry, max_id=str(max_id))
      if len(new_tweets["statuses"]) > 0:
       for tweetDoc in new_tweets["statuses"]:
         try:
#       print(tweetDoc['place'])
            tweetDoc["_id"] = tweetDoc["id_str"]
            max_id = int(float(tweetDoc["_id"])) - 1
            if tweetDoc["place"] != "None":
               if tweetDoc["place"]["name"] == 'Boston':
                  print(tweetDoc["_id"], tweetDoc["place"]["name"])
                  dbdoc = dbt.save(tweetDoc)
         except:
            print(tweetDoc["_id"], "Duplication occured")
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
         time.sleep(60 * 6)

      else:
       #Users Loop
       for row in dbt.query(usernames, '_count', group=True):
         get_all_tweets(row.key)
         mylogsfile = open(logsfile, 'a')
         mylogsfile.write('User Break %s.\n' % (datetime.datetime.now()))
         mylogsfile.close()
         time.sleep(60 * 2) #300 calls limit per 15-min window
      time.sleep(60 * 60)
