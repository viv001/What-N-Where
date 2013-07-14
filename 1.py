#!/usr/bin/python
s = '[{ "latitude":"9","longitude":"-6","sentiment":"Bad","message":"gJpk6Q" } ,{ "latitude":"4","longitude":"39","sentiment":"Bad","message":"oxahbW" } ]'

def main():
    with open("/var/www/yahoo/data/tweets.json","w") as outfile:
        outfile.write(s)
        outfile.close()

if __name__ == "__main__":
        main()

