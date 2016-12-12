import pymongo,string,sys
from CoocCounts import NMI_Scores,CoOccurence_Counts,Marginal_Counts,Total_Counts,Cosine_Scores
import numpy as np

validationset = open(sys.argv[1],'r')
#validationGroundTruth = open(sys.argv[2],'a')
validationOutput = open(sys.argv[2],'a')
validationScores = open(sys.argv[3],'a')
#sys.stdout = validationOutput


# Get total Counts for the entity set (here all pairs)
TotalCounts = np.array([Total_Counts()])

for line in validationset:
	validationScores.write("**" + line + "\n")
	original = line.split()
	line = line.replace(",", ' ')
	line = line.translate(string.maketrans("",""), string.punctuation)
	#missing_word = line[1]
	token = line.split()
	line_id = token[0]
	if int(line_id) < 110543:
		continue
	#missing_word = token[1]
	print token
	pair = {}

	for i in range(1,len(token)-1):
	#for i in range(2,len(token)-1):
		# Get Cooccurence count of the pair
		CooccurenceCount = np.array(CoOccurence_Counts(token[i],token[i+1]))
		# Get Marginal Count for all 
		MarginalCountA = np.array(Marginal_Counts(1,token[i]))
		MarginalCountB = np.array(Marginal_Counts(2,token[i+1]))
		e = 0.01
		Pab = (CooccurenceCount+e)/TotalCounts
		Pa_ = (MarginalCountA+e)/TotalCounts
		P_b = (MarginalCountB+e)/TotalCounts

		# Cooccurence Consistency
		pair[token[i]+","+token[i+1]] = Cosine_Scores(Pab,Pa_,P_b)[0]
	
	best_pair = []
	minimum = 999
	cos_score = np.array([])
	for key in pair:
    	#print key, 'corresponds to', d[key]
		if pair[key][0] < pair[key][1] and minimum > pair[key][1]:# and pair[key][0][1] > pair[key][0][2]:
			minimum = pair[key][1]
			best_pair = key.split(",")
			cos_score = pair[key]
			#print best_pair,cos_score
	
	validationScores.write(",".join(best_pair) + " Cosine_Scores: " + np.array_str(cos_score)+"\n")
	validationScores.write("***********************\n\n")
	print original
	not_inserted = True
	try:
		index = original.index(best_pair[0])
		original.insert(index+1,"_")
		not_inserted = False
	except :
		pass
	if not_inserted:
		try:
			index = original.index(best_pair[1])
			original.insert(index,"_")
		except :
			pass
		
	validationOutput.write(" ".join(original)+"\n")