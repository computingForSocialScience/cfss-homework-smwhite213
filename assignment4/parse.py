import csv
import sys

import matplotlib.pyplot as plt



def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

HPpermits= readCSV("permits_hydepark.csv")


### enter your code below

def get_avg_latlng(x):
	"""Finds the average latitude and longitude"""
	LATITUDE=[]
	LONGITUDE=[]

	#pull the latitude and longitude from the tuples in the provided list
	for i in range(len(x)):
		lat=float(x[i][-2])
		LATITUDE.append(lat)
		lon=float(x[i][-3])
		LONGITUDE.append(lon)

	#Uncomment to test code	
	#print LATITUDE
	#print LONGITUDE	

	#calculate the average latitude and longitude
	for var in x:
		avglat=sum(LATITUDE)/float(len(LATITUDE))
		avglong=sum(LONGITUDE)/float(len(LONGITUDE))
	print (avglat,avglong)


#Use this code to run programs on whole list of permits
#permits=readCSV("permits.csv")
#print len(permits)

#Find latitude and longitude in Hyde Park only
#get_avg_latlng(HPpermits)


def zip_code_barchart(x):
	"""Creates a bar chart of zipcodes"""
	zipcode_list={}

	#Loop through data to strip out zipcodes and clean data
	for i in range(1,len(x)):
		zipcode=x[i][28]

		#Clean data by stripping zipcodes of extra characters
		#and converting to integers
		modzip=zipcode[0:5]
		if not modzip:
			modzip=0
		elif modzip=='IL':
			modzip=0
		elif '-' in modzip:
			modzip=0
		intzip=int(modzip)

		#uncomment below to test code
		#print intzip

		#Develop dictionary of zipcodes and their counts
		if intzip in zipcode_list:
			zipcode_list[intzip]+=1
		else:
			zipcode_list[intzip]=1

	#Uncomment to test code	
	#print zipcode_list

	#Create a bar graph of zipcodes and frequency
	plt.bar(range(len(zipcode_list)),zipcode_list.values(),align='center')
	plt.xticks(range(len(zipcode_list)),zipcode_list.keys())
	plt.title("Frequency of Zipcodes")
	#plt.show()

	#Save graph in directory
	plt.savefig("barchart.jpg")


#zip_code_barchart(HPpermits)

if sys.argv[1]=="latlong":
	get_avg_latlng(HPpermits)
elif sys.argv[1]=="hist":
	zip_code_barchart(HPpermits)