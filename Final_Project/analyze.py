import pandas as pd
import numpy as np  
from scipy import stats
from scipy.stats import ttest_ind
import csv
from io import open
import matplotlib.pyplot as plt 
from pandas.io.data import DataReader as dr
import statsmodels.api as sm 
import pandas.stats.ols as pdols
from pandas.stats.plm import PanelOLS



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
#print sumstats

correlations=df.corr()
#print correlations

cat1=df[df['Party']=="R"]
cat2=df[df['Party']=="D"]

ttests=[]
#df_ttests=pd.DataFrame(columns=['T-Statistic','P-Value'])


ttestNeg=ttest_ind(cat1['Avg Neg'],cat2['Avg Neg'])
senttypeN=('Negative',)
insertN=senttypeN+ttestNeg
ttests.append(insertN)
print ttestNeg

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
plt.savefig('boxplots_byparty.png')
#plt.show()
bp=df.boxplot(column=['Avg Neg'],by='State')
plt.savefig('boxplot_bystate.png')

#Dummy variable for being a Republican

df2=pd.concat([df,pd.get_dummies(df['Party'],dummy_na=False)],axis=1)
#print df2

#x=pd.get_dummies(df['Party'], dummy_na=False)
#print x

#xsumstats=df['x'].describe()

#print xsumstats
x=df2['R']
#print x
y=df2['Avg Neg']
gradient, intercept, r_value, p_value, std_error=stats.linregress(x,y)
#print "Gradient and intercept and p-value"
print gradient, intercept, p_value

state_ttests=[]
for state in df2['State']:
	#if df2[df2['State']==state]:
	#statelist=df2['State'].tolist()
	#print statelist
	#ttestNegS=ttest_ind(cat1['Avg Neg'],cat2['Avg Neg'])
	cat1state=cat1[cat1['State']==state]
	cat2state=cat2[cat2['State']==state]
	ttestNegS=ttest_ind(cat1state['Avg Neg'],cat2state['Avg Neg'])
	#info=df2.loc[df['State']==state].extract('State')
	#state=info['State']
	#print info
	#col1=str(state)
	tstat,pvalue=ttestNegS
	insertS=(state,tstat,pvalue)
	state_ttests.append(insertS)

cat2=df[df['Party']=="D"]

df3=pd.DataFrame(state_ttests)
print df3

#print df2
#model=sm.OLS(y,x).fit()
#print model.summary()


#df3=pd.concat([df2,pd.get_dummies(df2['State'],dummy_na=False)],axis=1)

#x=df3[['R']][:-1]
#y=df3['Avg Neg']
#gradient, intercept, r_value, p_value, std_error=stats.linregress(x,y)
#print "Gradient and intercept and p-value"
#print gradient, intercept, p_value
#reg=PanelOLS(y=df2['Avg Neg'],x=df2['R'],cluster=['State'])
#print reg
#reg=PanelOLS(y=df['Avg Neg'],x=df['R'],entity_effects=True)
#reg=PanelOLS(y=df2['Avg Neg'],x=df2['R'])

#print reg

#model=pd.ols(y=df['Avg Neg'],x=df['Party'])
#print model

#df2.log
