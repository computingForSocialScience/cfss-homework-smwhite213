import pandas as pd
import numpy as np  
from scipy import stats
import csv
from io import open



infile=open('sentiments_testruns.csv','r')
#infile=open('sentiments.csv','r')

reader=csv.reader(infile)

readlist=[]
for line in reader:
	readlist.append(line)

#print readlist	
df=pd.DataFrame(readlist)
print df
sumstats=df.describe()
print sumstats
correlations=df.corr()
print correlations
