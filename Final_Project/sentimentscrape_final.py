import tweepy
#from flask import Flask, render_template, request, redirect, url_for
#import pymysql
import json
import requests 
import csv
from io import open
import unicodedata
import unicodecsv
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

#print "test script"


#####################################################################
#KEY INFORMATION & AUTHORIZATION
#####################################################################

SunlightApiKey = "2afd981a0bad449b9a213cd0cda5c48c"

TwitAccessToken="109627122-2dvwCKktLzZlORvzTRlOC8AMLdAuqbWaeU7xfUtL"
TwitAccessSecret="Ms8K1dGyYH3F2BpWvBAv1Jx01nMWHNtSca2912qykKLt9"

TwitConsumerKey="cv7sCmTV4Wqrr7QTNPmV1AQf3"
TwitConsumerSecret="c9IrvGQQrosI0uqR5pjVf1clYDXNjgZEqwrtCxGJyIDIhXVxRz"

auth=tweepy.OAuthHandler(TwitConsumerKey,TwitConsumerSecret)
auth.set_access_token(TwitAccessToken,TwitAccessSecret)

########Note that, because of the large number of calls, wait_on_rate_limit is 
    #necessary when running the full program (but not the "test version" as
    #described below.)
api=tweepy.API(auth,wait_on_rate_limit=True)

#Using the Sunlight Congress API, fetches members of the 114th Congress
    #returns a dictionary with Congress information.

url="https://congress.api.sunlightfoundation.com/legislators?&per_page=50&page=11&apikey="+SunlightApiKey


def getuserid(twitSN):
    """Given a user's screen name, returns Twitter ID for fetching statuses"""
    getid=api.get_user(twitSN)
    testid=getid.id
    return testid



#####################################################################
#CODE TO FETCH TWEETS FROM CONGRESSPEOPLE AND ANALYZE THEM
#####################################################################

#congresslist will be a list of tuples for each congressperson with a valid Twitter ID 
    #and a strictly positive number of tweets.
congresslist=[]

#Uncomment count2 and failcount to test code. When full code is running,
    #there should be 539 congresspeople, a few of whom may not have valide 
    #Twitter IDs (failcount).

#count2=0
#failcount=0


#####################################################################
#Notes on the loop below:
#Run only one of the two versions at a time (i.e., only one set of the below lines of code
    #should be uncommented at a given time):
    #The "full version" for this project takes about 30 minutes to run. Uncomment the following:
        #for page in range(1,12):
        #for person in congresspeople:
        #rawstatuses=api.user_timeline(twitterid,count=1000)
        
        #Note that if this code is running, it's okay to uncomment 
        #outfile=open('sentiments.csv','wb')
        #This is in the "Write results to local csv file" section below.

    #The "test version" for this project takes about 3 minutes to run. Uncomment the folliowing:
        #for page in range(1,4):
        #for person in congresspeople[0:10]:
        #rawstatuses=api.user_timeline(twitterid,count=10)   

        #If this code is running, please make sure the above outfile code is commented out.
        #Instead, use outfile=open('sentiments_testruns.csv','wb')
#####################################################################


#The below loop makes sure to loop through pages of Sunlight Foundation request.
for page in range(1,4):
#for page in range(1,12):

    #Fetch information about reps in the 114th Congress from Sunlight Foundation:
    #print page
    newreq=requests.get(url,params={'page':page})
    data=newreq.json()
    congresspeople=data['results']
    

    #For each congressperson, the below loop finds twitter ID, fetch tweets, and find average 
    #sentiment of tweets via vaderSentiment.  
    
    #One and only one of the two below lines should be uncommented:  
    for person in congresspeople[0:10]:
    #for person in congresspeople:
        
        #count2+=1
        rawlastname=person['last_name']
        #lastname=person['last_name']
        lastname=rawlastname.encode('utf-8')
        rawfirstname=person['first_name']
        #firstname=person['first_name']
        firstname=rawfirstname.encode('utf-8')
        #rawstate=person['state']
        state=person['state']
        #state=rawstate.encode('utf-8')
        #rawparty=person['party']
        party=person['party']
        #party=rawparty.encode('utf-8')

        try:
            twitterSN=person['twitter_id']
        except KeyError:
            #failcount+=1           
            continue
        
        #Skip congresspeople for whom twitter ID isn't missing but is listed as "None."
        twitterSN_str=str(twitterSN)
        #count_NoneSN=0

        #print twitterSN_str
        if twitterSN_str=="None":
            #count_NoneSN+=1
            continue
        if not twitterSN:
            continue

        #print twitterSN

        #Skip congresspeople without valid Twitter ID.
        try:
            twitterid=getuserid(twitterSN)
        except tweepy.error.TweepError:
            continue
        if not twitterid:
            continue

        #One and only one of the two below lines should be uncommented:  
        #rawstatuses=api.user_timeline(twitterid,count=1000)
        rawstatuses=api.user_timeline(twitterid,count=10)

        #Create a list to temporarily store the status updates of each congressperson.
        tweetlist=[]
        for status in rawstatuses:
            statustext=status.text
            statustext=statustext.encode('utf-8')
            tweetlist.append(statustext)

        ########################################
        #Run sentiment analysis on tweets via vaderSentiment
        ########################################

        #Intermediate variables used to find average sentiment (below)
        totalneg=0
        totalneu=0
        totalpos=0
        totalcomp=0
        persontweets=0
        
        #Loop finds sentiment of each tweet and aggregates scores
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

        #Calculates average sentiments for all collected tweets and drops observations without 
        #any tweets
        if not persontweets==0:
            avgneg=totalneg/persontweets
            avgneu=totalneu/persontweets
            avgpos=totalpos/persontweets
            avgcomp=totalcomp/persontweets
        else:
            continue
        
        #Stores relevant information about each congressperson in a tuple and adds to list
        tup=(lastname,firstname,twitterSN,state,party,avgneg,avgneu,avgpos,avgcomp,persontweets)
        congresslist.append(tup)
        
        #innercount+=1
        #print innercount
    
    #Uncomment below line in order to monitor progress of loop   
    #print page

#Test loop:
#print congresslist[0:3]

########################################
#Write results to local csv file
########################################

#***********************#
#IMPORTANT: For the purpose of testing code, write to "sentiments_testruns.csv" and
#not to "sentiments.csv", which is storing information for all 500+ congresspeople
#and sentiment analysis for up to 1,000 tweets per congressperson.

#***********************#

#outfile=open('sentiments.csv','wb')
outfile=open('sentiments_testruns.csv','wb')
writer=csv.writer(outfile)

#Add Header with more descriptive column names
#writer.writerow(['Last Name','First Name','Twitter Username','State','Party',
#    'Average Negative Sentiment','Average Neutral Sentiment','Average Positive Sentiment',
#    'Average Compound Sentiment','Total Tweets Collected'])

#Preferred for testing: Add Header with less descriptive column names
writer.writerow(['Lastname','Firstname','TwitterID','State','Party','Avg Neg','Avg Neut','Avg Pos','Avg Compound','#Tweets'])

#Insert congress tweet info into csv
for person in congresslist:
    #row=person.encode('utf-8')
    writer.writerow(person)

outfile.close()

########################################
#Print total # accounts (and other info if need to test code)
########################################


#print "Total count"
#print count2
#print "Tweepy Key Errors"
#print failcount
print "Total number with accounts"
length=len(congresslist)
print length
#print "Accounts listed as None"
#print count_NoneSN


########################################
#Aggregate info for each party
#In the below variables, let "D" refer to Democrat, "R" to Republican, and "I" to Independent
#Finally, display results.
########################################

countD=0
countR=0
countI=0

totalnegD=0
totalnegR=0
totalnegI=0
totalneuD=0
totalneuR=0
###TO DO: Find other totals for neutral, positive, compound
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

if not countD==0:
    avgnegD=float(totalnegD)/float(countD)
    print "Average negative sentiment for Democrats"
    print avgnegD
else:
    print "(There are no Democrats in this sample.)"
if not countR==0:
    avgnegR=float(totalnegR)/float(countR)
    print "Average negative sentiment for Republicans"
    print avgnegR
else:
    print "(There are no Republicans in this sample.)"
if not countI==0:
    avgnegI=float(totalnegI)/float(countI)
    print "Average negative sentiment for Independents"
    print avgnegI
else:
    print "(There are no Independents in this sample.)"

print "Democrats with accounts"
print countD
print "Repubs with accounts"
print countR
print "Independents with accounts"
print countI

