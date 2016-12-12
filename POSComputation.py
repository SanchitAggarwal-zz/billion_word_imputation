import pymongo,string,sys
import re
import nltk
from nltk import pos_tag, word_tokenize
from pymongo import MongoClient,ASCENDING, DESCENDING

# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

#Getting the Databse and Collection
WordImputation = client['WordImputationNGrams']
BigramFrequency = WordImputation['BigramFrequency']
#WordFrequency =  WordImputation['WordFrequency']

# creating Compound Index on Pair of words
BigramFrequency.create_index([("firstword", ASCENDING), ("secondword", ASCENDING)])

trainingset = open(sys.argv[1],'r')

# Building Pairwise Frequency for Word Calculation for window size of 7
window = 2 #Window size 7
linenumber = 0
for line in trainingset:
	linenumber = linenumber + 1
	# Remove Punctuation from line
	line = line.translate(string.maketrans("",""), string.punctuation)
	line = line.lower()
	line = re.sub('([^\D]|_)+', "", line)
	line = word_tokenize(line)
	post = nltk.pos_tag(line)
	if len(post)>1:
		 for i in range(0, len(post)-1):
		 	for j in range(i+1, i+window):
		 		if j<len(post):
		 			firstword = post[i][1]
		 			secondword = post[j][1]
		 			pair = BigramFrequency.find({
		 				"firstword":firstword,
		 				"secondword":secondword
		 			})
		 			if pair.count() == 0:
		 				pair = {
		 					"firstword": firstword,
		 					"secondword":secondword,
		 					"frequency":1
		 				}
		 				BigramFrequency.insert(pair)
		 				print ("Insert",firstword,secondword,'bigram')
	 				else:
	 					key = 'frequency'
	    				BigramFrequency.update({"firstword":firstword,"secondword":secondword},{'$inc':{key: 1}},upsert=False, multi=False)
					print ("Update",firstword,secondword,'bigram')
	   				#word = words[i]
		    		#wordcount = WordFrequency.find({"word":word})
    				#if wordcount.count() == 0:
    				#	WordFrequency.insert({"word":word,"frequency":1})
   					#else:
   					#	WordFrequency.update({"word":word},{'$inc':{"frequency": 1}},upsert=False, multi=False)

	#words =  line.split()
	#print (linenumber,"************* ",line," ***********",len(words))
	#print word_tokenize(line)
	# if len(words) > 1:
	# 	for i in range(0,len(words)-1):
	# 		for j in range(i + 1,i + window + 1):
	# 			if j<len(words):
	# 				firstword = words[i]
	# 				secondword = words[j]
	# 				distance = j-i
	# 				pair = PairWiseFrequency.find({
	# 													"firstword":firstword,
	# 													"secondword":secondword
	# 												})
	# 				if pair.count() == 0:
	# 					pair = {
	# 							"firstword": firstword,
	# 							"secondword": secondword,
	# 							"frequency": {str(distance) : 1}
	#    							}
	#    					PairWiseFrequency.insert(pair)
	#    					print ("Insert",firstword,secondword,distance)
	#    				else:
	#    					key = 'frequency.' + str(distance)
	#    					PairWiseFrequency.update({"firstword":firstword,"secondword":secondword},{'$inc':{key: 1}},upsert=False, multi=False)
	#    					print ("Update",firstword,secondword,distance)
	#    		word = words[i]
	#    		wordcount = WordFrequency.find({"word":word})
	#    		if wordcount.count() == 0:
	#    			WordFrequency.insert({"word":word,"frequency":1})
 #   			else:
 #   				WordFrequency.update({"word":word},{'$inc':{"frequency": 1}},upsert=False, multi=False)

