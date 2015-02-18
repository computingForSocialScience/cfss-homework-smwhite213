import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    #opens csv files with relevant data
    f_artists = open('artists.csv')
    f_albums = open('albums.csv')

    #defines variable of rows of the CSV file
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums)

    #allows code below to skip header row
    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    #begins list for artist names
    artist_names = []
    
    #creates list of decades spanning 1900-2020
    decades = range(1900,2020, 10)
    decade_dict = {}
    #makes the base count for each decade zero
    for decade in decades:
        decade_dict[decade] = 0
    
    #loops through each row of artists, identifies contents of each row, and plucks out name
    for artist_row in artists_rows:
        if not artist_row:
            continue
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)

    #loops through each row of albums, identifies contents, and counts albums 
    #released in a given decade (by looping through decades variable)     
    for album_row  in albums_rows:
        if not album_row:
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break

    #defines lists to be used for plotting the below chart
    x_values = decades
    y_values = [decade_dict[d] for d in decades]
    return x_values, y_values, artist_names

def plotBarChart():
    
    #sends relevant values to be charted
    x_vals, y_vals, artist_names = getBarChartData()
    
    #identifies chart type (bar) and parameters
    fig , ax = plt.subplots(1,1)
    ax.bar(x_vals, y_vals, width=10)
    #labels axes
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    #creates label for whole chart
    ax.set_title('Totals for ' + ', '.join(artist_names))
    #displays chart in new window
    plt.show()


    
#getBarChartData()
#plotBarChart()