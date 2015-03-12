from flask import Flask, render_template, request, redirect, url_for
import pymysql
import networkx as nx
import numpy as np 
import requests

from fetchArtist import *
from fetchAlbums import *
from artistNetworks import *
#from analyzeNetworks import *
#from makePlaylist import *

dbname="playlists"
host="localhost"
user="root"
passwd="di0nYsu$"
#port=4499
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()
app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))


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

def createNewPlaylist(artistName):

    """Given an artist name, creates a new playlist of 30 songs"""

    #Creates new tables for playlists and songs if they don't already exist 
    sql_createPlaylists = '''CREATE TABLE IF NOT EXISTS playlists (playlistId INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(200));'''
    cur.execute(sql_createPlaylists)
    sql_createSongs = '''CREATE TABLE IF NOT EXISTS songs (playlistId int, song_order INTEGER PRIMARY KEY AUTO_INCREMENT, artistName VARCHAR(200), albumName VARCHAR(200), songName VARCHAR(300));'''
    cur.execute(sql_createSongs)

    #Insert new root artist info into playlist database
    addArtist = '''INSERT INTO playlists (rootArtist) VALUES (%s);''' 
    cur.execute(addArtist,artistName)

    #Snatch playlist ID
    #playlistId= '''SELECT playlistId from playlists;'''
    #cur.execute(playlistId)

    playlistId = cur.lastrowid

    #Obtain artist ID and relevant info
    artistID = fetchArtistId(artistName)
    edges = getDepthEdges(artistID,2)
    newartists=[]
    for i in range(len(edges)):
        newartists.append(edges[i][1])

    count=0
    while count<= 30:

        #Pick a random artist, album, and song from the list of edges (up to 30)
        song_order=count+1

        picknewartist=np.random.choice(newartists)
        artistInfo=fetchArtistInfo(picknewartist)
        artistName=artistInfo['name']

        albums=fetchAlbumIds(picknewartist)
        if not albums:
            continue
        pickalbum=np.random.choice(albums)
        albumInfo=fetchAlbumInfo(pickalbum)
        albumName=albumInfo['name']

        songName=getRandomSong(pickalbum)

        newrow=(playlistId,song_order,artistName,albumName,songName)
        sql_addrow = '''INSERT INTO songs (playlistId, song_order, artistName, albumName, songName) VALUES (%s, %s,%s,%s,%s);'''
        cur.execute(sql_addrow,newrow)

        count+=1


# print the songs table to test 
    cur.execute('''SELECT * FROM songs;''')
    sql_result = cur.fetchall()
    print (sql_result)


#mysql_createPlaylists = '''CREATE TABLE IF NOT EXISTS playlists (playlistId INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(100));'''
#cur.execute(mysql_createPlaylists)

#mysql_createSongs = '''CREATE TABLE IF NOT EXISTS songs (playlistId int, song_order INTEGER PRIMARY KEY AUTO_INCREMENT, artistName VARCHAR(100), albumName VARCHAR(100), songName VARCHAR(200));'''
#cur.execute(mysql_createSongs)

createNewPlaylist("Led Zeppelin")


if __name__ == '__main__':
    app.debug=True
    app.run()