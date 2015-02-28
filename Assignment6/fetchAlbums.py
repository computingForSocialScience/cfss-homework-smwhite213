import requests
from datetime import datetime

from fetchArtist import fetchArtistId
from fetchArtist import fetchArtistInfo

###NOTE: I HAD DIFFICULTIES IMPORTING FUNCTIONS FROM OTHER python files
###SCROLL DOWN TO SEE NEW CODE


    

####NEW CODE STARTS HERE


def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url="https://api.spotify.com/v1/artists/"+artist_id+"/albums?offset=0&album_type=album&market=US"
    req=requests.get(url)
    data=req.json()
    items=data['items']
    albums_ids=[]
    for album in items:
    	rawuri=album['uri']
    	uri=rawuri[14:]
    	albums_ids.append(uri)
    return albums_ids

    #print data

#fetchAlbumIds(fetchArtistId('Led Zeppelin'))

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url="https://api.spotify.com/v1/albums/"+album_id
    req=requests.get(url)
    data=req.json()
    albuminfo={}

    artistinfo=data['artists']
    firstartist=artistinfo[0]
    artist_id=firstartist['id']
    albuminfo['artist_id']=artist_id

    rawuri=data['uri']
    albuminfo['album_id']=rawuri[14:]

    albuminfo['name']=data['name']

    releasedate=data['release_date']
    year=releasedate[0:4]
    albuminfo['year']=year

    albuminfo['popularity']=data['popularity']
    return albuminfo

#fetchAlbumInfo(fetchAlbumIds(fetchArtistId('Led Zeppelin'))[0])
