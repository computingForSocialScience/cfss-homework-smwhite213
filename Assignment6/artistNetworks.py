
import sys
import requests
import csv
import pandas as pd 

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url="https://api.spotify.com/v1/search?query="+'"'+name+'"'+"&type=artist"
    req=requests.get(url)
    data=req.json()
    
    artists=data['artists']
    items=artists['items']
    if items==[]:
    	print "Artist not found; try retyping"
    		
    firstitems=items[0]
    artid=firstitems['uri']
    
    artist_id=artid[15:]
    return artist_id

def getRelatedArtists(artistID):
	url="https://api.spotify.com/v1/artists/"+artistID+"/related-artists"
	req=requests.get(url)
	data=req.json()
	artists=data['artists']
	related_artists=[]
	for arts in artists:
		art_id=arts['id']
		related_artists.append(art_id)
		if len(related_artists)>=20:
			break
	return related_artists



def getDepthEdges(artistID, depth):

	if depth<1:
		print "Please enter a number no less than 1."
	
	tuples=[]
	totalartistlist=[]
	totalartistlist.append(artistID)

	count=1

	while count<=depth:
		updateartists=[]
		for item in totalartistlist:
			newartists=getRelatedArtists(item)
			for artist in newartists:
				updateartists.append(artist)
				newtuple=(item,artist)
				if newtuple in tuples:
					continue
				else:
					tuples.append(newtuple)
		
		for newarts in updateartists:
			totalartistlist.append(newarts)
		count=count+1

	return tuples
	
test=getDepthEdges(fetchArtistId("Led Zeppelin"),2)
#print len(test)

def getEdgeList(artistID, depth):

	edgeList=pd.DataFrame(getDepthEdges(artistID,depth))

	return edgeList
	

test2=getEdgeList(fetchArtistId("Led Zeppelin"),2)

def writeEdgeList(artistID, depth, filename):

	edgeList=getEdgeList(artistID,depth)

	edgeList.to_csv(filename, index=False)

	return edgeList

writeEdgeList(fetchArtistId("The Rolling Stones"),2,"edgelist.csv")



