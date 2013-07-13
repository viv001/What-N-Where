#!/usr/bin/python
import tweepy
import json
import urllib
import urllib2

consumer_key = 'xojc5iRiowk5Feu8pxshmg'
consumer_secret = '0cBTG690VY7gAhOXJa8AWAD92mOcTjuqw1XJx1JxIY'

access_token_key = '1590672726-xPss9wL0sgSXyh5IWgCcHHZpTGc1kf886FDy2XM'
access_token_secret = 'tdAlAqHcY4xbsOb0KCyz76lFpWh2FVhIEflRdWYjsA'

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)
d_list=[]
class StreamListener(tweepy.StreamListener):
    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return True
    def on_timeout(self):
        print sys.stderr, "Timeout..."
	return True
    def on_data(self, data):
     try:
       t = json.loads(data)
       d = {}
       sent_link = "https://api.sentigem.com/external/get-sentiment"
       values = {"api-key":"1084700d32bfd211fcddbe643f66430fLvaKbsk6GN-ehnR_IJFyOtlQmzMA4PoZ","text":t["text"]}
       param = urllib.urlencode(values)
       req = urllib2.Request(sent_link,param)
       f = urllib2.urlopen(req)
       polar = json.load(f)
       if polar["polarity"]=="neutral":
           return True
       d["data"] = {"message":t["text"],"longitude":t["geo"]["coordinates"][0],"latitude":t["geo"]["coordinates"][1],"polarity":polar["polarity"]}
       with open("tweets.json","w") as outfile:
           json.dump(d,outfile)
       outfile.close()
       return True
     except KeyboardInterrupt:
	print "Keyboard interrupt give .. closing!! "
	return False
     except:
       print "No new tweets !! "
       return True

def extract_tweet(latitude,longitude):
	global d_list
	l = StreamListener()
	streamer = tweepy.Stream(auth=auth1, listener=l)
	setLocation = [longitude-0.5,latitude-0.5,longitude+0.5,latitude+0.5]
	try:
	 streamer.filter(locations = setLocation)
   	except KeyboardInterrupt:
	  print "Keyboard Interrupt given. Ending!! "
	  return
	except: 
   	  print "Force close !! Lot of data extracted!! :):D"
	  return 

