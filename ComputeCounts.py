import pymongo,string,sys
import nltk
from nltk import pos_tag, word_tokenize
import math
from pymongo import MongoClient,ASCENDING, DESCENDING
import numpy as np


f = file(sys.argv[4], 'a')
sys.stdout = f
# Connecting to Database
clientA = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(clientA.database_names())

clientB = MongoClient('localhost', int(sys.argv[1]))  #Default host and port for Mongod instance
print(clientB.database_names())


#Getting the Databse and Collection
WordImputation = clientB[sys.argv[2]]
PairWiseFrequency = WordImputation[sys.argv[3]]
PairWiseFrequency.create_index([("firstword", ASCENDING), ("secondword", ASCENDING)])


#Getting the Databse and Collection
CooCCount = clientA['CooCCount']
MarginalCounts = CooCCount['MarginalCounts']
TotalCount = CooCCount['TotalCount']
MarginalCounts.create_index([("word", ASCENDING)])

Pairs = PairWiseFrequency.find()
Count = Pairs.count()
TotalCounts = [0,0,0]
for i in range(0,Count):
	firstword = Pairs[i]["firstword"]
	secondword = Pairs[i]["secondword"]
	frequency = Pairs[i]["frequency"]

	CooccurenceCount = [0,0,0]
	for j in range(1, 4):
			if str(j) in frequency:
				CooccurenceCount[j-1] = frequency[str(j)]
				#increment correspponding total count
				TotalCounts[j-1] = TotalCounts[j-1] + frequency[str(j)]

	MarginalCounts.update({"word":firstword},{'$inc':{"1*": CooccurenceCount[0],
						"2*": CooccurenceCount[1],"3*": CooccurenceCount[2],"*1": 0,
						"*2": 0,"*3": 0}},upsert=True, multi=False)
	
	MarginalCounts.update({"word":secondword},{'$inc':{"*1": CooccurenceCount[0],
						"*2": CooccurenceCount[1],"*3": CooccurenceCount[2],"1*": 0,
						"2*": 0,"3*": 0}},upsert=True, multi=False)

	TotalCount.update({"*_*":"*"},{'$set':{"1": TotalCounts[0],
						"2": TotalCounts[1],"3": TotalCounts[2]}},upsert=True, multi=False)

	print Pairs[i]['_id'],i,TotalCounts

f.close()