import pymongo,string,sys
import nltk
from nltk import pos_tag, word_tokenize
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
PairWiseFrequency = WordImputation['PairWiseFrequency']
TotalCount = WordImputation['TotalCount']

def NMI_Scores(Pab,Pa_,P_b):
	#Calculates the co-occurence Consistency by calculating Co-occurence Counts, Marginal counts and Total counts for Pair a,b
	#Use Normalized Point wise Mutual Information
	# PAB = np.array(Pab)
	# PA_ = np.array(Pa_)
	# P_B = np.array(P_b)

	PAB = Pab
	PA_ = Pa_
	P_B = P_b

	Numerator = PAB/(PA_*P_B)
	Denominator = 1/PAB
	print "Numerator:",Numerator
	print "Denominator:",Denominator
	NMI = np.log(Numerator)/np.log(Denominator)
	#print "NMI:",NMI
	return NMI

def Cosine_Scores(Pab,Pa_,P_b):
	#Calculates the co-occurence Consistency by calculating Co-occurence Counts, Marginal counts and Total counts for Pair a,b
	#Use Normalized Point wise Mutual Information
	# PAB = np.array(Pab)
	# PA_ = np.array(Pa_)
	# P_B = np.array(P_b)

	PAB = Pab
	PA_ = Pa_
	P_B = P_b

	Cosine = PAB/np.sqrt(PA_*P_B)
	#print "Cosine:",Cosine
	return Cosine
	
def CoOccurence_Counts(firstword,secondword):
	#Calculating Co-occurence Count for each skip from 1 to 3
	Pairs = PairWiseFrequency.find({
									"firstword":firstword,
									"secondword":secondword
								  })
	Count = Pairs.count()
	CooccurenceCount = [0,0,0]
	for i in range(0,Count):
		try:
			frequency = Pairs[i]["frequency"]
			for j in range(1, 4):
				if str(j) in frequency:
					CooccurenceCount[j-1] = frequency[str(j)]
		except:
			CooccurenceCount = [0,0,0]
			pass
	#print "CooccurenceCount:",CooccurenceCount
	return CooccurenceCount


def Marginal_Counts(postion,word):
	if postion == 1:
		MC = MarginalCountsA.find({"word_*":word})
	else:
		MC = MarginalCountsB.find({"*_word":word})

	Count = MC.count()
	MarginalCount = [0,0,0]
	for i in range(0,Count):
		try:
			for j in range(1, 4):
				MarginalCount[j-1] = MC[i][str(j)]
		except:
			MarginalCount = [0,0,0]
			pass
	#print "MarginalCount:",MarginalCount
	return MarginalCount


def Total_Counts():
	TC = TotalCount.find()
	Count = TC.count()
	TotalCounts = [0,0,0]
	for i in range(0,Count):
		try:
			for j in range(1, 4):
				TotalCounts[j-1] = float(TC[i][str(j)])
		except:
			pass
	#print "TotalCounts",TotalCounts
	return TotalCounts

def compute_score(word_a,word_b,x):
	# Get Cooccurence count of the pair
	TotalCounts = np.array([Total_Counts()])

	CooccurenceCount = np.array(CoOccurence_Counts(word_a,word_b))
	# Get Marginal Count for all 
	MarginalCountA = np.array(Marginal_Counts(1,word_a))
	MarginalCountB = np.array(Marginal_Counts(2,word_b))
	e = 0.0001
	Pab = (CooccurenceCount+e)/TotalCounts
	Pa_ = (MarginalCountA+e)/TotalCounts
	P_b = (MarginalCountB+e)/TotalCounts

	# Cooccurence Consistency
	score = Cosine_Scores(Pab,Pa_,P_b)[0]
	if x == -1:
		return score
	else:
		return score[x]

def Candidate_words(word_a,word_b):
	# Word_A_count = PairWiseFrequency.find({"firstword":word_a,"frequency.1":{"$gt":1}}).count()
	# Word_A_MC = Marginal_Counts(1,word_a)[0]
	# GT = (Word_A_MC+1)/(Word_A_count+1)
	# GT = GT * 100
	GT = 500
	Limit = 5
	Words_A = PairWiseFrequency.find({"firstword":word_a,"frequency.1":{"$gt":GT}}).sort("frequency.1", DESCENDING).limit(Limit)
	Candidate_words = []
	if Words_A.count() > Limit:
		count = Limit
	else:
		count = Words_A.count()
	#print count
	for i in range(0,count):
		word = Words_A[i]["secondword"]
		#coocCount = CoOccurence_Counts(word,word_b)
		Words_B = PairWiseFrequency.find({"firstword":word,"secondword":word_b})
		if Words_B.count() > 0:
		#if coocCount[0] > coocCount[1]:
			Candidate_words.append(word)
	# for i in Candidate_words:
	# 	print i
	# print "***********"
	return Candidate_words


