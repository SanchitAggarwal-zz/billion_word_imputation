import pymongo,string
from pymongo import MongoClient,ASCENDING, DESCENDING
from scoringFunction import distanceScore
from itertools import izip


# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

# Getting the Databse and Collection
WordImputation = client['WordImputationTrainVal']
PairWiseFrequency = WordImputation['PairWiseFrequency']
WordFrequency =  WordImputation['WordFrequency']

# creating Compound Index on Pair of words
PairWiseFrequency.create_index([("firstword", ASCENDING), ("secondword", ASCENDING)])

validationset = open('./data/Validation_Set.txt','r')
validationsetGroundTruth = open('./data/Validation_GroundTruth.txt','r')

# Building Pairwise Frequency for Word Calculation for window size of 7
window = 3 #Window size 7
linenumber = 0
Accuracy = 0
for line,gline in izip(validationset,validationsetGroundTruth):
	score = {}
	linenumber = linenumber + 1
	# Remove Punctuation from line
	line = line.split(",")
	beg = line[0]
	line = line.pop()
	line = line.translate(string.maketrans("",""), string.punctuation)
	line = line.lower()
	words =  line.split()

	gline = gline.split(",")
	gbeg = gline[0]
	gline = gline.pop()
	gline = gline.translate(string.maketrans("",""), string.punctuation)
	gline = gline.lower()
	gwords = gline.split()

	print (linenumber,"************* ",line," ***********",len(words))
	if len(words) > 1:
		for i in range(0,len(words)-2):
					j = i+1
					print j
					firstword = words[i]
					secondword = words[j]
					pair = PairWiseFrequency.find({
														"firstword":firstword,
														"secondword":secondword
													})
					if pair.count() == 0:
						#print "not valid pair"
						#score[firstword +" " + secondword] = 0
						score[i] = 0
					else:
						frequency = pair[0]['frequency']
						value = distanceScore(frequency,window)
						if value < 0.5:
							#score[firstword +" " + secondword] = value
							score[i] = value
							print gwords
							print words
							if gwords[i] == firstword and gwords[j+1] == secondword:
								Accuracy = Accuracy + 1
								break
print Accuracy/linenumber

						
						

