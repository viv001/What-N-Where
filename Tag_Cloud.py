#!/usr/bin/python

#======================================================================
# Tag Cloud creator using the posts.csv dataset
#======================================================================

# necessary imports
import csv
import re
import string
import math



# Global vars
word_popularity={}    # Dictionary for storing word popularity value
word_TF={}            # Dictionary for storing word TF value
word_IDF={}           # Dictionary for storing word IDF value
word_TFIDF={}         # Dictionary for storing word TF-IDF value
word_finalvalue={}    # Dictionary for storing word final statistical value
fb_id=[]              # list of all fb ids
post_time=[]          # list of all fb post times
post_type=[]          # list of all fb post type
likes=[]              # list of number of likes of ith facebook id
comments=[]           # list of number of comments of ith facebook id
shares=[]             # list of number of shares of ith facebook id



#Method to parse time 

def parse_time(t):
    x = t.split()
    a = x[0].split('-')
    b = x[2].split(':')
    year = int(a[0])
    month = int(a[1])
    date = int(a[2])
    hour = int(b[0])
    minute = int(b[1])



# Methods which parses the posts.csv file and populate all the dictionary with the popularity values,
# TF and IDF values of all the words

def parse_csv():
    with open('/var/www/yahoo/data/posts.csv', 'rb') as csvfile:
        spamreader= csv.reader(csvfile, delimiter=',', quotechar='"')
        s = ""
        like = 0
        comment = 0
        share = 0
        x = 0
        v = 1
        words = []
        count = 0
        for row in spamreader:
            w = row[0]
            w = w.lower()
            count = count + 1
            if count>50:
                break
            if w in word_TF:
                word_TF[w] = word_TF[w] + 1
            else:
                word_TF[w] = 1
            if w in word_IDF:
                word_IDF[w] = word_IDF[w] + 1
            else:
                word_IDF[w] = 1
            if len(w)>3:
                if w in word_popularity:
                    word_popularity[w] = word_popularity[w] + v
                else:
                    word_popularity[w] = v
    csvfile.close()
                
# This method calulates all the popularity, TF-IDF values of all the words.
# Then, it plots the tag cloud for top 200 words and stores the plot in tag_cloud.png file.

def create_tagcloud():
    from pytagcloud import create_tag_image, make_tags
    from pytagcloud.lang.counter import get_tag_counts
    word_list=[]
    for w in word_IDF:
        word_IDF[w] = math.log( float(10) / float(word_IDF[w]) )

    # calculation of TF-IDF values
    for w in word_TF:
        word_TFIDF[w] = word_TF[w] * word_IDF[w]

    # calculation of final statistical values
    for w in word_popularity:
        word_finalvalue[w] = word_TFIDF[w] + word_popularity[w]

    for w in sorted(word_finalvalue, key=word_finalvalue.get, reverse=True):
        x = (w,word_finalvalue[w])
        word_list.append(x)
        if len(word_list)>200:
            break
    tags = make_tags(word_list, maxsize=120)

    create_tag_image(tags, '/var/www/yahoo/images/tag_cloud.png', size=(1500, 1200), fontname='Lobster')


# Main method

def main():
    parse_csv()
    create_tagcloud()


if __name__ == "__main__":
        main()


#END=================================================================
