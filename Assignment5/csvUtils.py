from io import open
import sys
import requests
import csv
from fetchArtist import fetchArtistId
from fetchArtist import fetchArtistInfo
from fetchAlbums import fetchAlbumInfo
from fetchAlbums import fetchAlbumIds





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



#writeArtistsTable(artist_dictionary)    
  

#Create dictionary with multiple albums to test

#Un-comment to test code
#album_list=[]
#album_list=fetchAlbumIds(fetchArtistId('Led Zeppelin'))
#album_list_dictionary=[]
#for albums in album_list:
#    album_info=fetchAlbumInfo(albums)
#    album_list_dictionary.append(album_info)
#print album_list_dictionary

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
        album=album_info_list[i]
        album_id=album['album_id']
        album_name=album['name']
        year=album['year']
        popularity=album['popularity']
        f.write(album_id+','+album_id+','+'"'+album_name+'"'+','+str(year)+','+str(popularity)+'\n')
        
    return f

#writeAlbumsTable(album_list_dictionary)