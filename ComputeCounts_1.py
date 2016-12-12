import pymongo,string,sys
import nltk
from nltk import pos_tag, word_tokenize
import math
from pymongo import MongoClient,ASCENDING, DESCENDING
import numpy as np

# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

#Getting the Databse and Collection
WordImputation = client['WordImputationNGramsV2']
#collections
MarginalCountsA = WordImputation['MarginalCountsA']
MarginalCountsB = WordImputation['MarginalCountsB']
TotalCount = WordImputation['TotalCount']
PairWiseFrequency = WordImputation['PairWiseFrequency']

db.MarginalCountsB.ensureIndex( { "*_word": 1 } )
db.MarginalCountsA.ensureIndex( { "word_*": 1 } )

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

	MarginalCountsA.update({"word_*":firstword},{'$inc':{"1": CooccurenceCount[0],
						"2": CooccurenceCount[1],"3": CooccurenceCount[2]}},upsert=True, multi=False)
	MarginalCountsB.update({"*_word":secondword},{'$inc':{"1": CooccurenceCount[0],
						"2": CooccurenceCount[1],"3": CooccurenceCount[2]}},upsert=True, multi=False)

	for j in range(1, 4):
		if str(j) in frequency:
			TotalCounts[j-1] = TotalCounts[j-1] + frequency[str(j)]
	TotalCount.update({"*_*":"*"},{'$set':{"1": TotalCounts[0],
						"2": TotalCounts[1],"3": TotalCounts[2]}},upsert=True, multi=False)
	if i%1000 == 0 :
		print TotalCounts