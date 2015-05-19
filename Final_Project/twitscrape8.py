#from __future__ import print_function
#import statsmodels.api as statsmodels
#import matplotlib.pyplot as plt
#from statsmodels.sandbox.regression.predstd import wls_prediction_std
import tweepy
from flask import Flask, render_template, request, redirect, url_for
import pymysql
#import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import requests 
import csv
import urllib3
from urllib2 import urlopen
import unicodedata
import unicodecsv
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

urllib3.disable_warnings()
#http=urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

print "test script"

SunlightApiKey = "2afd981a0bad449b9a213cd0cda5c48c"

TwitAccessToken="109627122-2dvwCKktLzZlORvzTRlOC8AMLdAuqbWaeU7xfUtL"
TwitAccessSecret="Ms8K1dGyYH3F2BpWvBAv1Jx01nMWHNtSca2912qykKLt9"

TwitConsumerKey="cv7sCmTV4Wqrr7QTNPmV1AQf3"
TwitConsumerSecret="c9IrvGQQrosI0uqR5pjVf1clYDXNjgZEqwrtCxGJyIDIhXVxRz"

auth=tweepy.OAuthHandler(TwitConsumerKey,TwitConsumerSecret)
auth.set_access_token(TwitAccessToken,TwitAccessSecret)
api=tweepy.API(auth,wait_on_rate_limit=True)
#api.update_status('tweepy + oauth!')

#def fetch114Congress():
#Using the Sunlight Congress API, fetches members of the 114th Congress
#returns a dictionary with Congress information.


    #url="https://congress.api.sunlightfoundation.com/legislators?&apikey="+SunlightApiKey+"&congress=114"
url="https://congress.api.sunlightfoundation.com/legislators?&per_page=50&page=11&apikey="+SunlightApiKey

#for page in range(1,12):
    #req1=urlopen(url,params={'page': page}).read()
    #req1.append(requests.get(url,params={'page':page}))
    
#data=req1.json()
    #req=http.request('GET',url)
    #req=requests.get(url)
    #req1=urlopen(url.encode('utf-8')).read()

    #data=json.loads(req1)
    #print data

#congresspeople=data['results']
    #unicodedata.normalize('NFKD',input).encode('ascii','ignore')
    #count1=0

def getuserid(twitSN):
    """Given a user's screen name, returns ID"""
    getid=api.get_user(twitSN)
    testid=getid.id
    return testid

congresslist=[]
count2=0
failcount=0

for page in range(1,4):
#for page in range(1,12):
    #req1=urlopen(url,params={'page': page}).read()
    newreq=requests.get(url,params={'page':page})

    data=newreq.json()
    congresspeople=data['results']
    innercount=0
    
    #Use next line to run streamlined version of code while testing. 
    for person in congresspeople[0:10]:
    #for person in congresspeople:
        count2+=1
        lastname=person['last_name']
        firstname=person['first_name']
        try:
            twitterSN=person['twitter_id']
        except KeyError:
            failcount+=1           
            continue
        twitterSN_str=str(twitterSN)
        count_NoneSN=0
        if "None" in twitterSN_str:
            count_NoneSN+=1
            continue
        #twitterSN=person['twitter_id']
        #congressinfo[x]['lastname']=person['last_name']
        #twitterid=person['twitter_id']
        state=person['state']
        party=person['party']

        if not twitterSN:
            continue
        #print twitterSN
        try:
            twitterid=getuserid(twitterSN)
        except tweepy.error.TweepError:
            continue
        if not twitterid:
            continue
        #rawstatuses=api.user_timeline(twitterid,count=1000)
        rawstatuses=api.user_timeline(twitterid,count=10)
        tweetlist=[]
        for status in rawstatuses:
            statustext=status.text
            statustext=statustext.encode('utf-8')
            tweetlist.append(statustext)

        totalneg=0
        totalneu=0
        totalpos=0
        totalcomp=0
        persontweets=0
        for tweets in tweetlist:
            #print tweets
            persontweets+=1
            vs=vaderSentiment(tweets)
            negative=float(vs['neg'])
            totalneg+=negative
            neutral=float(vs['neu'])
            totalneu+=neutral
            positive=float(vs['pos'])
            totalpos+=positive
            compound=float(vs['compound'])
            totalcomp+=compound
        if not persontweets==0:
            avgneg=totalneg/persontweets
            avgneu=totalneu/persontweets
            avgpos=totalpos/persontweets
            avgcomp=totalcomp/persontweets
        else:
            continue
        tup=(lastname,firstname,twitterid,state,party,avgneg,avgneu,avgpos,avgcomp)
        congresslist.append(tup)
        innercount+=1
        #print innercount
        
        	#print twitterid
    print page
print "Total count"
print count2
print "Tweepy Key Errors"
print failcount
print "Total number with accounts"
length=len(congresslist)
print length
print "Accounts listed as None"
print count_NoneSN

countD=0
countR=0
countI=0

totalnegD=0
totalnegR=0
totalnegI=0
totalneuD=0
totalneuR=0
#... continue

for x in range(len(congresslist)):
    if congresslist[x][4]=="D":
        totalnegD=totalnegD+congresslist[x][5]
        countD+=1
    elif congresslist[x][4]=="R":
        totalnegR=totalnegR+congresslist[x][5]
        countR+=1
    elif congresslist[x][4]=="I":
        totalnegI=totalnegI+congresslist[x][5]
        countI+=1

avgnegD=float(totalnegD)/float(countD)
avgnegR=float(totalnegR)/float(countR)
if not countI==0:
    avgnegI=float(totalnegI)/float(countI)
print "Democrats with accounts"
print countD
print "Repubs with accounts"
print countR
print "Independents with accounts"
print countI
#Of the 539 Congresspeople in the 114th Congress, 510 have Twitter ids, and only 159 could
#be matched to twitter accounts.
print "Average neg Dems"
if not countD==0:
    print avgnegD
else:
    print "(There are no Republicans in this sample.)"

print "Average neg Repubs"
if not countR==0:
    print avgnegR
else:
    print "(There are no Republicans in this sample.)"

print "Average neg Indeps"
if not countI==0:
    print avgnegI
else:
    print "(There are no independents in this sample.)"

#from scipy import stats
#from pylab import plot, show


#for member in congresslist:


#x=()
#y_neg=()

#slope, incercept, r_value, p_value, std_err = stats.linregress(x,y)

#from bokeh.plotting import figure
#from bokeh.resources import CDN 
#from bokeh.embed import file_html, components

app = Flask(__name__)

@app.route('/')
def mainpage():
    return 'Test page!'

if __name__=='__main__':
    app.run()

