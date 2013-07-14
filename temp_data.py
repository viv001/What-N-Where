#!/usr/bin/python
import random
import time
import json
import string

def write_to_tag_cloud(s):
   s = s.translate(string.maketrans("",""), string.punctuation)
   l = s.split()
   with open("/var/www/yahoo/data/posts.csv", "a") as myfile:
      for e in l:
        myfile.write(e.encode("ascii","ignore")+"\n")
   myfile.close()


sentences=[]
sentences.append("Had a great time at yahoo hack india 2013 !! #Hyderbaad :) :)")
sentences.append("Enjoyed #yahoohack-2013 #Hyd")
sentences.append("Ohhh !! Just fell short of time making a nice API. But had fun #HackYAHOOOO #Hyd" )
sentences.append("Two days at Westin!! For #YahooHack contest !! Nice weekend ")
sentences.append("#Yahoo made the weekend for me !! Will be waiting for another #Yahoo-hack")
lat = 163.66
lon = 774.76
for i in range(200):
   d={}
   d["data"]={"message":sentences[random.randint(0,4)],"latitude":(lat+random.randint(0,20))/10.,"longitude":(lon+random.randint(0,20))/10.,"sentiment":"positive"}
   l = [d]
   with open("/var/www/yahoo/data/tweets.json","w") as outfile:
      write_to_tag_cloud(d['data']['message'])
      json.dump(l,outfile)
   outfile.close()
   time.sleep(2)
