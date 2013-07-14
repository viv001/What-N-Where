#!/usr/bin/python
import tweepy
import json
import urllib
import urllib2
import sys

#Details for twitter API !! 

consumer_key = 'xojc5iRiowk5Feu8pxshmg'
consumer_secret = '0cBTG690VY7gAhOXJa8AWAD92mOcTjuqw1XJx1JxIY'

access_token_key = '1590672726-xPss9wL0sgSXyh5IWgCcHHZpTGc1kf886FDy2XM'
access_token_secret = 'tdAlAqHcY4xbsOb0KCyz76lFpWh2FVhIEflRdWYjsA'

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)
d_list=[]

#Using twitter API

def write_to_tag_cloud(s):
   s = s.translate(string.maketrans("",""), string.punctuation)
   l = s.split()
   with open("tag_cloud.csv", "a") as myfile:
   for e in l:
      myfile.write(e.encode("ascii","ignore")+"\n")
   myfile.close()


class StreamListener(tweepy.StreamListener):
    def on_error(self, status_code):		#Function if any error occurs in twitter API
        print 'Error: ' + repr(status_code)
        return True
    
    def on_timeout(self):			#Function for twitter connection time out !! 
        print sys.stderr, "Timeout..."
	return True
    
    def on_data(self, data):			#Function for fetching the tweets and taking the required data !! 
     try:
       data = data.encode("ascii", "ignore")
       t = json.loads(data)
       d = {}

#Sentiment analysis of the tweets !! 
       sent_link = "https://api.sentigem.com/external/get-sentiment"
       txt = t["text"].encode("ascii","ignore")
       write_to_tag_cloud(txt)
       values = {"api-key":"1084700d32bfd211fcddbe643f66430fLvaKbsk6GN-ehnR_IJFyOtlQmzMA4PoZ","text":txt}
       param = urllib.urlencode(values)
       req = urllib2.Request(sent_link,param)
       f = urllib2.urlopen(req)
       polar = json.load(f)
       if polar["polarity"]=="neutral":
           return True
       d["data"] = {"message":txt,"longitude":t["geo"]["coordinates"][1],"latitude":t["geo"]["coordinates"][0],"sentiment":polar["polarity"]}
       l = []
       l.append(d)
       #File writing of the extracted data ! !
       with open("/var/www/yahoo/data/tweets.json","w") as outfile:
          json.dump(l,outfile)
       outfile.close()
       return True
     except KeyboardInterrupt:
	   print "Keyboard interrupt give .. closing!! "
	   return False
     except Exception as e:
       print e
       return True

def extract_tweet(latitude,longitude):
	l = StreamListener()
	streamer = tweepy.Stream(auth=auth1, listener=l)
	setLocation = [longitude-1.5,latitude-1.5,longitude+1.5,latitude+1.5]
	try:
	  streamer.filter(locations = setLocation)
   	except KeyboardInterrupt:		#To end on keyboard interrupt
	  print "Keyboard Interrupt given. Ending!! "
	  return
   	except Exception as e:		#To end on keyboard interrupt
	  print  e
	  return

#Program calls the functions here and takes the input
lat = float(sys.argv[1])
lon = float(sys.argv[2])
extract_tweet(lat,lon)
