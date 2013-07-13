import json
import time
from pprint import pprint
import urllib
import urllib2

def get_location(post):
      url = "http://query.yahooapis.com/v1/public/yql"
      query = 'SELECT * FROM geo.placemaker WHERE documentContent = "' + post + '" AND documentType="text/plain"'
      values = {'q':query,
                'format':'json'}
      data = urllib.urlencode(values)
      req = urllib2.Request(url, data)
      response = urllib2.urlopen(req)
      the_page = json.load(response)
      loc = the_page["query"]["results"]["matches"]["match"]["place"]["centroid"]
      return (loc["latitude"],loc["longitude"])


token  = "CAACEdEose0cBAFMZCDRED8RagZBitozYZAZAeP6Jn6KQYlZC5yZCgXdqwk3aIEZAusYtfj5jQ1CWI86ViDs4a6LUVbZARaXJAhiHKHpBYUdp4NZBUNZCIRVHW238ZBLKHPZAo7B16PmLHfS9bQX0wkOSm9HTA8sD3nj4mbLu37RisK4oZBQZDZD"
base_link = 'https://graph.facebook.com/search?q="the"|"a"&type=post'
access = '&access_token='+ token
post_link = base_link + access

while 1:
 try:
   f = urllib2.urlopen(post_link)
   data = json.load(f)
   d = {}
   for k in data["data"]:
      (lat, lon) = get_location(k["message"])
      if not lat:
          continue
      #print lat
      d["data"]= {"message":k["message"], "latitude":lat, "longitude":lon}
      with open("fbposts.json", "w") as outfile:
        json.dump(d, outfile)
      outfile.close()
 except KeyboardInterrupt:
   break
 except urllib2.HTTPError:
   print "Renew access code please"
   break
 except:
   continue


