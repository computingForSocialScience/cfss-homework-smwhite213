import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url="https://api.spotify.com/v1/search?query="+'"'+name+'"'+"&type=artist"
    req=requests.get(url)
    data=req.json()
    artists=data['artists']
    items=artists['items']
    firstitems=items[0]
    artid=firstitems['uri']
    artist_id=artid[15:]
    return artist_id

#fetchArtistId('Led Zeppelin')

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url="https://api.spotify.com/v1/artists/"+artist_id
    req=requests.get(url)
    data=req.json()
    artistinfo={}
    artistinfo['followers']=data['followers']
    artistinfo['genres']=data['genres']
    artistinfo['id']=artist_id
    artistinfo['name']=data['name']
    artistinfo['popularity']=data['popularity']
    print artistinfo

fetchArtistInfo(fetchArtistId('Led Zeppelin'))

