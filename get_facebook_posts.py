import json
import time
import math
from pprint import pprint
import urllib
import urllib2
import sys
import string

def write_to_tag_cloud(s):
    s = s.translate(string.maketrans("",""), string.punctuation)
    l = s.split()
    with open("tag_cloud.csv", "a") as myfile:
      for e in l:
          myfile.write(e.encode("ascii","ignore")+"\n")
    myfile.close()

def get_sentiment(s):
     sent_link = "https://api.sentigem.com/external/get-sentiment"
     values = {"api-key":"1084700d32bfd211fcddbe643f66430fLvaKbsk6GN-ehnR_IJFyOtlQmzMA4PoZ","text":s}
     param = urllib.urlencode(values)
     req = urllib2.Request(sent_link,param)
     f = urllib2.urlopen(req)
     polar = json.load(f)
     return polar["polarity"]

def get_location(post):
      url = "http://query.yahooapis.com/v1/public/yql"
      query = 'SELECT * FROM geo.placemaker WHERE documentContent = "' + post + '" AND documentType="text/plain"'
      values = {'q':query,
                'format':'json'}
      data = urllib.urlencode(values)
      req = urllib2.Request(url, data)
      response = urllib2.urlopen(req)
      the_page = json.load(response)
      try:
        loc = the_page["query"]["results"]["matches"]["match"]["place"]["centroid"]
        return (loc["latitude"].encode('ascii','ignore'), loc["longitude"].encode('ascii','ignore'))
      except:
        return ("", "")


#START

cur_lat = sys.argv[1]
cur_lon = sys.argv[2]

token  = "CAACEdEose0cBAKRYlU41yWi9NCWYJorx0QWAPyeeAMaHcSKeMe6EZAwVowNSwxt5zoA0KR8in8n1lBTinPSOcw7Ggiwe0kZCmmulI0GHsTZBzbDyWEXivo2IuEEiGsPB0EZB4iKe0aJsIj5fXo1IzkPH979XyNbLJ5mEaiu49wZDZD"
base_link = 'https://graph.facebook.com/search?q="the"|"a"&type=post'
access = '&access_token='+ token
post_link = base_link + access

while 1:
 try:
   f = urllib2.urlopen(post_link)
   data = json.load(f)
   d = {}
   for k in data["data"]:
      msg = k["message"].encode('ascii', 'ignore')
      (lat, lon) = get_location(msg)
      if not lat:
          continue
      if math.fabs( float(lat) - float(cur_lat) ) > 1 or math.fabs(float(lon) - float(cur_lon)) > 1:
	  continue
      sent = get_sentiment(msg)
      write_to_tag_cloud(msg)
      if sent != "positive" and sent != "negative":
        continue
      d["data"]= {"message":msg, "latitude":lat, "longitude":lon, "sentiment":sent}
      with open("fbposts.json", "w") as outfile:
        json.dump(d, outfile)
      outfile.close()
 except KeyboardInterrupt:
   break
 except urllib2.HTTPError as e:
   print e
   continue
 except:
   continue

