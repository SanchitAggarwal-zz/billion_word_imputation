import pymongo,string,sys
import random, os, string
import re
import nltk
from nltk import pos_tag, word_tokenize
from pymongo import MongoClient,ASCENDING, DESCENDING

trainfile = open(sys.argv[1],'r')
validationset = open(sys.argv[2],'a')
validationGroundTruth = open(sys.argv[3],'a')

start = 1
end = 5000
i = 1
random_lines = [random.randrange(start,end) for p in range(0,10)] #training-validation split is 70-30ss
for line in trainfile:
	if i in random_lines:
		line = line.replace("'s", '')
		line = line.translate(string.maketrans("",""), string.punctuation)
		line = line.lower()
		line = re.sub('([a-z]*[^\D][a-z]*|_)+', "", line)
		line = re.sub(r'[^\w]', ' ', line)
		token = line.split()
		original = line.split()
		if len(token) > 2:
			location = random.randint(1,len(token)-2);
			missingWord = token.pop(location)
			validationGroundTruth.write(str(i) + "," + str(missingWord) + "," + " ".join(original) + '\n')
			validationset.write(str(i) + "," + str(missingWord) + "," + " ".join(token) + '\n')
	i = i + 1
	if i > end:
		start = end
		end = end +  5000
		random_lines = [random.randrange(start,end) for p in range(0,10)] #training-validation split is 70-30
