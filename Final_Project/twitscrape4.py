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
api=tweepy.API(auth)
#api.update_status('tweepy + oauth!')

#def fetch114Congress():
#Using the Sunlight Congress API, fetches members of the 114th Congress
#returns a dictionary with Congress information.

    #url="https://congress.api.sunlightfoundation.com/legislators?&apikey="+SunlightApiKey+"&congress=114"
url="https://congress.api.sunlightfoundation.com/legislators?&per_page=50&page=11&apikey="+SunlightApiKey

for page in range(1,11):
    #req1=urlopen(url,params={'page': page}).read()
    req1=requests.get(url,params={'page':page})

data=req1.json()
    #req=http.request('GET',url)
    #req=requests.get(url)
    #req1=urlopen(url.encode('utf-8')).read()

    #data=json.loads(req1)
    #print data

congresspeople=data['results']
    #unicodedata.normalize('NFKD',input).encode('ascii','ignore')
    #count1=0
congresslist=[]
count2=0
for person in congresspeople:
    lastname=person['last_name']
    firstname=person['first_name']
    twitterid=person['twitter_id']
    #congressinfo[x]['lastname']=person['last_name']
    #twitterid=person['twitter_id']
    state=person['state']
    party=person['party']
    tup=(lastname,firstname,twitterid,state,party)
    congresslist.append(tup)
    count2+=1
    	#print twitterid
print count2
print congresslist[0:5]
    #artists=data['artists']
    #items=artists['items']
    #if items==[]:
    #	print "Artist not found; try retyping"
    		
    #firstitems=items[0]
    #artid=firstitems['uri']
    
    #artist_id=artid[15:]
    #return artist_id


#fetch114Congress()
print congresslist[0][2]
test=congresslist[0][2]

def getuserid(twitSN):
    """Given a user's screen name, returns ID"""
    getid=api.get_user(twitSN)
    testid=getid.id
    return testid


testid=getuserid(test)
print testid
me=api.me()
myid=me.id
#print me
print myid

print testid
test_statuses=api.user_timeline(testid)


test_list=[]
for status in test_statuses:
    statustext=status.text
    statustext=statustext.encode('utf-8')
    #unicodedata.normalize('NFKD',statustext).encode('ascii','ignore')
    #print statustext
    test_list.append(statustext)

print test_list[1:5]

totalneg=0
totalneu=0
totalpos=0
totalcomp=0

for tweets in test_list:
    #print tweets
    vs=vaderSentiment(tweets)
    negative=float(vs['neg'])
    totalneg+=negative
    neutral=float(vs['neu'])
    totalneu+=neutral
    positive=float(vs['pos'])
    totalpos+=positive
    compound=float(vs['compound'])
    totalcomp+=compound
    #print vs
print totalneg
print totalneu
print totalpos
print totalcomp

    #print vs
    #print "\n\t" + str(vs)


#for status in test_statuses:

#for members in congresslist:
#    twitterid=congresslist[2]
#    for status in tweepy.Cursor(api.statuses_lookup, id=twitterid).items(10):
#        print stat
#for person in congresspeople:

    #statuses=API.statuses_lookup(twitterid)

#print statuses
#db1=pymysql.connect("localhost",user="root",passwd="")

#cur=db1.cursor()
#sql="CREATE DATABASE tweets"
#cur.execute(sql)

