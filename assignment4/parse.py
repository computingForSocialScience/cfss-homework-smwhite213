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



### enter your code below

def get_avg_latlng(x):
	LATITUDE=[]
	LONGITUDE=[]
	for i in range(len(x)):
		lat=float(x[i][-2])
		LATITUDE.append(lat)
		lon=float(x[i][-3])
		LONGITUDE.append(lon)
	#print LATITUDE
	#print LONGITUDE	
	for var in x:
		avglat=sum(LATITUDE)/float(len(LATITUDE))
		avglong=sum(LONGITUDE)/float(len(LONGITUDE))
	print (avglat,avglong)

permits=readCSV("permits.csv")
HPpermits= readCSV("permits_hydepark.csv")
#print HPpermits
#print len(HPpermits)

get_avg_latlng(HPpermits)

print len(permits)

def zip_code_barchart(x):
	zipcode_list={}
	#for data in x:
	#	rowdata=[cell.text for cell in x]
	#	zipcode=rowdata[28]
	#	zipcode_list.append(zipcode)

	#print zipcode_list[3:6]
	for i in range(1,len(x)):
		zipcode=x[i][28]
		modzip=zipcode[0:5]
		if not modzip:
			modzip=0
		elif modzip=='IL':
			modzip=0
		elif '-' in modzip:
			modzip=0
		intzip=int(modzip)
		#print intzip
		if intzip in zipcode_list:
			zipcode_list[intzip]+=1
		else:
			zipcode_list[intzip]=1
		
		#zipcode_list.append(zipcode)
	#print zipcode_list
	plt.bar(range(len(zipcode_list)),zipcode_list.values(),align='center')
	plt.xticks(range(len(zipcode_list)),zipcode_list.keys())
	#zipcode_list[0],zipcode_list[1])
	#plt.hist(zipcode_list)
	plt.title("Frequency of Zipcodes")
	#plt.show()
	plt.savefig("barchart.jpg")


zip_code_barchart(HPpermits)
