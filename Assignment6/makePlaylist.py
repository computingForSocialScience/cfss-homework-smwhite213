import sys
import requests
import csv
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
from io import open

from artistNetworks import fetchArtistId
from artistNetworks import getRelatedArtists
from artistNetworks import getDepthEdges
from artistNetworks import getEdgeList
from artistNetworks import writeEdgeList
from analyzeNetworks import readEdgeList
from analyzeNetworks import degree
from analyzeNetworks import combineEdgeLists
from analyzeNetworks import pandasToNetworkX
from analyzeNetworks import randomCentralNode
from fetchAlbums import fetchAlbumIds
from fetchAlbums import fetchAlbumInfo
from fetchArtist import fetchArtistInfo

def getRandomSong(albumid):

	url="https://api.spotify.com/v1/albums/"+albumid+"/tracks"
	req=requests.get(url)
	data=req.json()
	items=data['items']
	songlist=[]
	for item in items:
		songlist.append(item['name'])
	picksong=np.random.choice(songlist)
	return picksong


testsong=getRandomSong("7gS8ozSkvPW3VBPLnXOZ7S")
print testsong

if __name__=="__main__":
	artistnames=sys.argv[1:]
	print "The artists are", artistnames

	listofartIDs=[]
	for name in artistnames:
		artID=fetchArtistId(name)
		listofartIDs.append(artID)

	edgeList_list=[]
	for artist in listofartIDs:
		edgeList=getEdgeList(artist,2)
		edgeList_list.append(edgeList)

	combinedlists=edgeList_list[0]
	for lists in edgeList_list[1:]:
		newlist=combineEdgeLists(combinedlists,lists)
		combinedlists=newlist

	g=pandasToNetworkX(combinedlists)

	random_artists=[]
	for i in range(30):
		newartist=randomCentralNode(g)
		random_artists.append(newartist)

	#print random_artists

	rows=[]
	
	f=open('playlist.csv','w',encoding='utf-8')
	f.write(u'ARTIST_NAME,ALBUM_NAME,TRACK_NAME\n') 

	for artist in random_artists:
		artistinfo=fetchArtistInfo(artist)
		artistname=artistinfo['name']
		albumlist=fetchAlbumIds(artist)
		if not albumlist:
			continue
		else:
			pickalbum=np.random.choice(albumlist)
		albuminfo=fetchAlbumInfo(pickalbum)
		albumname=albuminfo['name']
		songname=getRandomSong(pickalbum)
		f.write('"'+artistname+'"'+','+'"'+albumname+'"'+','+'"'+songname+'"'+'\n')
		

