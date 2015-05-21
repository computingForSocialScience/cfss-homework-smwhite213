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
from matplotlib.font_manager import FontProperties as fp 



#####################################################################
#Read and organize data from csv file
#####################################################################

#df=pd.DataFrame.from_csv('sentiments_testruns.csv',header=0)
df=pd.DataFrame.from_csv('sentiments.csv',header=0)


#Split data by party, leaving out independents
cat1=df[df['Party']=="R"]
cat2=df[df['Party']=="D"]

#####################################################################
#Create and save boxplots
#####################################################################

bp=df.boxplot(column=['Avg Neg','Avg Neut','Avg Pos','Avg Compound'],by='Party')
plt.savefig('boxplots_byparty.png')

bp=df.boxplot(column=['Avg Neg'],by='Party')
plt.savefig('boxplots_byparty_negonly.png')

#bp=df.boxplot(column=['Avg Neg'],by='State').fp.set_size('x-small')
bp=df.boxplot(column=['Avg Neg'],by='State')
plt.savefig('boxplot_bystate.png')


#####################################################################
#Descriptive Statistics
#####################################################################

sumstats=df.describe()
print "Basic summary statistics"
print sumstats
print "***********************************************************"

correlations=df.corr()
print "Correlation Matrix"
print correlations
print "***********************************************************"

#####################################################################
#Conduct ttests and write to csv files
#####################################################################


##Basic ttests by party
ttests=[]

ttestNeg=ttest_ind(cat1['Avg Neg'],cat2['Avg Neg'])
senttypeN=('Negative',)
insertN=senttypeN+ttestNeg
ttests.append(insertN)
#print ttestNeg

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
df_ttests.to_csv('ttests_basic.csv')


#Create Dummy Variables for Party
df2=pd.concat([df,pd.get_dummies(df['Party'],dummy_na=False)],axis=1)
#print df2
state_ttests=[]

#Create a streamlined list of states for a data frame of ttests by state
statelist=df2['State'].tolist()
statelist2=[]
for state in statelist:
	if state in statelist2:
		continue
	else:
		statelist2.append(state)
#print statelist2


#####################################

#Perform ttest by party within each state. In csv file, states without sufficient data
#will have blank rows.
for state in statelist2:
	cat1state=cat1[cat1['State']==state]
	cat2state=cat2[cat2['State']==state]
	try:
		ttestNegS=ttest_ind(cat1state['Avg Neg'],cat2state['Avg Neg'])
	except RuntimeWarning:
		continue
	

	tstat,pvalue=ttestNegS

	insertS=(state,tstat,pvalue)
	state_ttests.append(insertS)

#Write to csv file
df3=pd.DataFrame(state_ttests,columns=('State','T-Statistic','P-Value'))
df3.to_csv('ttests_bystate.csv')


#####################################################################
#Regression
#####################################################################

reg_list=[]

x1=df2['R']
#x2=df2['State']
#x=np.column_stack((x1,x2))
x=sm.add_constant(x1)
print x
#y=np.dot(x,df2['Avg Neg'])+e 
y=df2['Avg Neg']
#gradient, intercept, r_value, p_value, std_error=stats.linregress(x1,y)
#print "Gradient and intercept and p-value"
#print gradient, intercept, p_value
model=sm.OLS(y,x).fit()
print model.summary()

