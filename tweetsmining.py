from tweepy import StreamListener
from tweepy import Stream
import tweepy
import json
import couchdb

#Twitter credentials, keep private
CONSUMER_KEY = 'RWG77BWeRymf1FoFWIKZjigli'
CONSUMER_SECRET = 'TDyQCxKxB9o5zxIe9WCQETy3Paw8T57DuBB772SA5WZYqOIUSL'
ACCESS_TOKEN = '22651013-tL49l2oBX7ooochixyuzkTqhJBbJbq2oVrDSuEYlB'
ACCESS_TOKEN_SECRET = 'oZojkB9n9RP0hf4cfgdVoDT7bHZKbtTkavVPTJxSXxgHr'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#twitter db on couchdb
server = couchdb.Server()
try:
    db = server.create('twitter')
except:
    db = server['twitter']

#Streaming listerner
class StdOutListener(StreamListener):

    def on_data(self, data):
        # process stream data then insert to db
        tweetDoc = json.loads(data)
        try:
           #print(tweetDoc)
           tweetDoc["_id"] = str(tweetDoc['id'])
           dbdoc = db.save(tweetDoc)
        except:
           print(tweetDoc["_id"], "Duplication occured")
           pass
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    #Boston city filteration
    twitterStream.filter(locations=[-71.06,42.22,-71.04,42.38])
