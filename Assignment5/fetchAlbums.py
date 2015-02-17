import requests
from datetime import datetime

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
    url="https://api.spotify.com/v1/artists/"+artist_id+"&album_type=album&market=US"
    req=requests.get(url)
    data=req.json()
    artistinfo={}
    artistinfo['followers']=data['followers']
    artistinfo['genres']=data['genres']
    artistinfo['id']=artist_id
    artistinfo['name']=data['name']
    artistinfo['popularity']=data['popularity']
    return artistinfo
    
def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url="https://api.spotify.com/v1/artists/"+artist_id+"/albums"
    req=requests.get(url)
    data=req.json()
    items=data['items']
    albums_ids=[]
    for album in items:
    	#number=items[i]
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
    print albuminfo

fetchAlbumInfo(fetchAlbumIds(fetchArtistId('Led Zeppelin'))[0])
