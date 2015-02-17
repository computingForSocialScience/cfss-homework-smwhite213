from io import open
import sys
import requests
import csv
from fetchArtist import fetchArtistId
from fetchArtist import fetchArtistInfo
from fetchAlbums import fetchAlbumInfo
from fetchAlbums import fetchAlbumIds

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
    artistinfo['id']=artist_id
    artistinfo['name']=data['name']
    artistinfo['followers']=data['followers']
    artistinfo['genres']=data['genres']
    artistinfo['popularity']=data['popularity']
    return artistinfo

fetchArtistInfo(fetchArtistId('Led Zeppelin'))
artist_dictionary=[]
artist_dictionary.append(fetchArtistInfo(fetchArtistId('Led Zeppelin')))
artist_dictionary.append(fetchArtistInfo(fetchArtistId('Robert Johnson')))

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

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f=open('artists.csv','w',encoding='utf-8')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n') 


    for i in range(len(artist_info_list)):
        artist=artist_info_list[i]
        artist_id=artist['id']
        name=artist['name']
        followers=artist['followers']
        numfollowers=followers['total']
        popularity=artist['popularity']
        f.write(artist_id+','+'"'+name+'"'+','+str(numfollowers)+','+str(popularity)+'\n')
        
    return f


writeArtistsTable(artist_dictionary)    
  

#Create dictionary with multiple albums to test

album_list=[]
album_list=fetchAlbumIds(fetchArtistId('Led Zeppelin'))
#print ("Test line")
#print album_list
#for i in range(len())

def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f=open('albums.csv','w',encoding='utf-8')
    f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n') 


    for i in range(len(album_info_list)):
        album=fetchAlbumInfo(album_info_list[i])
        album_id=album['album_id']
        album_name=album['name']
        year=album['year']
        popularity=album['popularity']
        f.write(album_id+','+album_id+','+'"'+album_name+'"'+','+str(year)+','+str(popularity)+'\n')
        
    return f

writeAlbumsTable(album_list)