from tweepy import StreamListener
from tweepy import Stream
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
CONSUMER_KEY = '8w5xQbiWoLlC9eNYAZt6qBb3i'
CONSUMER_SECRET = 'L4h4ArOMalcdIYEg62QAWVHSLe75RiaxApZzYjelMjjmd3dXtG'
ACCESS_TOKEN = '580647653-1MLL52CT6mwBpviA9irw7wgz0z23J3F7wG8Dra1J'
ACCESS_TOKEN_SECRET = '1bC7wFvhDHYg6SKiQKrwDkT5sKmgHPg8UCHzuf6MnNclk'

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
           MyCity = tweetDoc['place']['name']
           #Boston City only
           if MyCity == 'Boston':
              dbdoc = db.save(tweetDoc)
        except:
           print(tweetDoc["_id"], "Duplication occured")
           pass
        return True

    def on_error(self, status):
        print(status)
        mylogsfile.write('Error Status: %s %s.\n' % (status,datetime.datetime.now()))

if __name__ == '__main__':
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    #Boston city filteration
    twitterStream.filter(locations=[-72,41,-70,41.5])
