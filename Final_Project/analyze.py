import pandas as pd
import numpy as np  
from scipy import stats
from scipy.stats import ttest_ind
import csv
from io import open
import matplotlib.pyplot as plt 



#infile=open('sentiments_testruns.csv','r')
#infile=open('sentiments.csv','r')

#reader=csv.reader(infile)

#readlist=[]
#for line in reader:
#	readlist.append(line)

#print readlist	
#df=pd.DataFrame(readlist)
#print df

df=pd.DataFrame.from_csv('sentiments_testruns.csv',header=0)
#print df2
#index=df.index
#print index

#df['Avg Neg']=df['Avg Neg'].astype('float')

#print df2.dtypes

#df2=df[5:9].astype(float).describe()

sumstats=df.describe()
print sumstats

correlations=df.corr()
print correlations

cat1=df[df['Party']=="R"]
cat2=df[df['Party']=="D"]

ttests=[]
#df_ttests=pd.DataFrame(columns=['T-Statistic','P-Value'])


ttestNeg=ttest_ind(cat1['Avg Neg'],cat2['Avg Neg'])
senttypeN=('Negative',)
insertN=senttypeN+ttestNeg
ttests.append(insertN)

ttestNeut=ttest_ind(cat1['Avg Neut'],cat2['Avg Neut'])
senttypeNe=('Neutral',)
insertNe=senttypeNe+ttestNeut
ttests.append(insertNe)

ttestPos=ttest_ind(cat1['Avg Pos'],cat2['Avg Pos'])
senttypeP=('Positive',)
insertP=senttypeP+ttestPos
ttests.append(insertP)

ttestComp=ttest_ind(cat1['Avg Compound'],cat2['Avg Compound'])
senttypeC=('Compound',)
insertC=senttypeC+ttestComp
ttests.append(insertC)

df_ttests=pd.DataFrame(ttests,columns=('Sentiment','T-Statistic','P-Value'))
print df_ttests

#boxplotdf=pd.DataFrame(df,columns=['AvgNeg','AvgPos'])
#df['X']=df['Party']
#plt.figure();
bp=df.boxplot(column=['Avg Neg','Avg Neut','Avg Pos','Avg Compound'],by='Party')
#plt.plot(df['Party'],kind='box')

plt.savefig('boxplots.png')
plt.show()

