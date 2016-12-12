import pymongo,string,sys
import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.tag import hunpos
from nltk.tag.hunpos import HunposTagger
from pymongo import MongoClient,ASCENDING, DESCENDING

# Connecting to Database
client = MongoClient('localhost', 27017)  #Default host and port for Mongod instance
print(client.database_names())

ht = HunposTagger('english.model')

#Getting the Databse and Collection
WordImputation = client['WordImputationNGramsV2']
BigramFrequency = WordImputation['POSBigramFrequency']
WordFrequency =  WordImputation['POSFrequency']
LineNumber2Gram = WordImputation['POSLineNumber2Gram']

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
	token = word_tokenize(line)
	bigrams = nltk.ngrams(token, 2)

	print "Filename: "+sys.argv[1]+" Line: "+str(linenumber)

	# lineno = { "Filename:" sys.argv[1], "linenumber":linenumber}
	# LineNumber2Gram.insert(lineno)


	for bi in bigrams:
		first = ht.tag(word_tokenize(bi[0]));
		second = ht.tag(word_tokenize(bi[1]));

		firstword = first[0][1]
		secondword = second[0][1]

		bigram = BigramFrequency.find({
				"firstword":firstword,
				"secondword":secondword
			})

		if bigram.count()==0:
			bigram = {
					"firstword":firstword,
					"secondword":secondword,
					"frequency":1
			}
			BigramFrequency.insert(bigram)
			#print("Insert", firstword, secondword, 'bigram')
		else:
			key="frequency"
			BigramFrequency.update({"firstword":firstword,"secondword":secondword},{'$inc':{key: 1}},upsert=False, multi=False)
			#print("Update", firstword, secondword, 'bigram')
		word = firstword
		wordcount = WordFrequency.find({"word":word})
		if wordcount.count() == 0:
			WordFrequency.insert({"word":word,"frequency":1})
		else:
			WordFrequency.update({"word":word},{'$inc':{"frequency": 1}},upsert=False, multi=False)
		word_ = secondword
		wordcount_ = WordFrequency.find({"word":word_})
		if wordcount_.count() == 0:
			WordFrequency.insert({"word":word_,"frequency":1})
		else:
			WordFrequency.update({"word":word_},{'$inc':{"frequency": 1}},upsert=False, multi=False)