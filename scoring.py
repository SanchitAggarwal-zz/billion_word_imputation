import pymongo,string
from pymongo import MongoClient,ASCENDING, DESCENDING
from scoringFunction import distanceScore

# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

# Getting the Databse and Collection
WordImputation = client['WordImputationTrainVal']
PairWiseFrequency = WordImputation['PairWiseFrequency']
WordFrequency =  WordImputation['WordFrequency']

# Getting all the tuples
items=PairWiseFrequency.find()

# Calculating scores for each tuple
for i in range(0,10):
	item = items[i]
	print(item)
	pairwise = item['frequency']
	firstWord = item['firstword']
	secondWord = item['secondword']
	print("Calculating Scores for {} and {}".format(firstWord, secondWord))
	for i in range(1, 8):
		if str(i) in pairwise:
			score = distanceScore(i, pairwise[str(i)])
			print(score)
