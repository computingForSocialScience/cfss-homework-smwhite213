import sys
import requests
import csv
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 

from artistNetworks import fetchArtistId
from artistNetworks import getRelatedArtists
from artistNetworks import getDepthEdges
from artistNetworks import getEdgeList
from artistNetworks import writeEdgeList

def readEdgeList(filename):
	edgeList=pd.read_csv(filename, usecols=['0','1'])
	if len(edgeList.columns)!=2:
		print ("Warning: Only first two columns imported.")
	return edgeList

test=readEdgeList("test.csv")
#print test
test2=readEdgeList("edgelist.csv")

def degree(edgeList, in_or_out):

	if in_or_out=="out":
		return edgeList.ix[:,0].value_counts()
	elif in_or_out=="in":
		return edgeList.ix[:,1].value_counts()
	else: 
		print "Error with in vs. out degrees."

#deg= degree(test,"in")
#print deg

def combineEdgeLists(edgeList1, edgeList2):

	combinededgelist=pd.concat([edgeList1,edgeList2]).drop_duplicates()
	return combinededgelist

#test3=combineEdgeLists(test,test2)
#print test3

def pandasToNetworkX(edgeList):
	networks=edgeList.to_records(index=False)
	g=nx.DiGraph()
	for sender,receiver in networks:
		g.add_edge(sender,receiver)
	g.nodes()
	g.edges()
	nx.draw(g,with_labels=False)
	#plt.show()
	return g


#pandasToNetworkX(test)

def randomCentralNode(inputDiGraph):

	centralnodes=nx.eigenvector_centrality(inputDiGraph)
	#print centralnodes
	totalnodes=0
	for node in centralnodes:
		totalnodes+=centralnodes[node]
	#print totalnodes
	normnode={}
	for node in centralnodes:
		normnode[node]=centralnodes[node]/totalnodes
	#print normnode

	randomnode=np.random.choice(normnode.keys(),p=normnode.values())
	return randomnode

randomCentralNode(pandasToNetworkX(test))


