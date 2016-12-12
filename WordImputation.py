import pymongo,string
from pymongo import MongoClient,ASCENDING, DESCENDING
import time


# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

# Getting the Databse and Collection
WordImputation = client['WordImputationTestTime']
PairWiseFrequency = WordImputation['PairWiseFrequency']
WordFrequency =  WordImputation['WordFrequency']

# creating Compound Index on Pair of words
PairWiseFrequency.create_index([("firstword", ASCENDING), ("secondword", ASCENDING)])

trainingset = open('../KaggleDataset/train_v2.txt','r')

# Building Pairwise Frequency for Word Calculation for window size of 7
window = 3 #Window size 7
linenumber = 0
for line in trainingset:
	a = time.clock()
	linenumber = linenumber + 1
	# Remove Punctuation from line
	line = line.translate(string.maketrans("",""), string.punctuation)
	line = line.lower()
	words =  line.split()
	#print (linenumber,"************* ",line," ***********",len(words))
	if len(words) > 1:
		for i in range(0,len(words)-1):
			for j in range(i + 1,i + window + 1):
				if j<len(words):
					firstword = words[i]
					secondword = words[j]
					distance = j-i
					pair = PairWiseFrequency.find({
														"firstword":firstword,
														"secondword":secondword
													})
					if pair.count() == 0:
						pair = {
								"firstword": firstword,
								"secondword": secondword,
								"frequency": {str(distance) : 1}
	   							}
	   					PairWiseFrequency.insert(pair)
	   					#print ("Insert",firstword,secondword,distance)
	   				else:
	   					key = 'frequency.' + str(distance)
	   					PairWiseFrequency.update({"firstword":firstword,"secondword":secondword},{'$inc':{key: 1}},upsert=False, multi=False)
	   					#print ("Update",firstword,secondword,distance)
	   		word = words[i]
	   		wordcount = WordFrequency.find({"word":word})
	   		if wordcount.count() == 0:
	   			WordFrequency.insert({"word":word,"frequency":1})
   			else:
   				WordFrequency.update({"word":word},{'$inc':{"frequency": 1}},upsert=False, multi=False)
   	b = time.clock()
   	print b-a

