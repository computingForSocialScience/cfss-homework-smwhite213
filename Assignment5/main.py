import sys
import requests
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    
    artistlist=[]
    album_list=[]
    for i in range(len(artist_names)):
    	artistinfo=fetchArtistInfo(fetchArtistId(artist_names[i]))

    	artistlist.append(artistinfo)
    	artist_id=artistinfo['id']
    	albums=fetchAlbumIds(artist_id)
    	
    	for album in albums:
    
    		albuminfo=fetchAlbumInfo(album)

    		album_list.append(albuminfo)
 	
    writeAlbumsTable(album_list)
    writeArtistsTable(artistlist)

plotBarChart()
    

