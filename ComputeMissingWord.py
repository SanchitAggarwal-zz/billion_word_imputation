import pymongo,string,sys
from CoocCounts import NMI_Scores,CoOccurence_Counts,Marginal_Counts,Total_Counts,Cosine_Scores,Candidate_words,compute_score
import numpy as np

validationset = open(sys.argv[1],'r')
#validationGroundTruth = open(sys.argv[2],'a')
validationOutput = open(sys.argv[2],'a')
validationScores = open(sys.argv[3],'a')
#sys.stdout = validationOutput


# Get total Counts for the entity set (here all pairs)
TotalCounts = np.array([Total_Counts()])

for line in validationset:
	#validationGroundTruth = open(sys.argv[2],'a')
	validationOutput = open(sys.argv[2],'a')
	validationScores = open(sys.argv[3],'a')

	validationScores.write(line + "\n")
	original = line.split()
	line = line.replace(",", ' ')
	line = line.translate(string.maketrans("",""), string.punctuation)
	#missing_word = line[1]
	token = line.split()
	line_id = token[0]
	#missing_word = token[1]
	print token
	CMP = {}

	for i in range(1,len(token)-1):
	#for i in range(2,len(token)-1):
		# Cooccurence Consistency
		
		score = compute_score(token[i],token[i+1],-1)
		# #print score
		
		if score[0] < score[1]:
			#Get Candidate Words
			CW = Candidate_words(token[i],token[i+1])
			CW_Scores = []
			# Print to output
			validationScores.write(token[i]+","+token[i+1] + " Cosine_Scores: " + np.array_str(score)+"\n")
			validationScores.write("Candidate Words: ")
			for word in CW:
				word = "".join([ch if ord(ch)<= 128 else "_" for ch in word])
				#word = word.decode('utf-8')
				validationScores.write(word + ", ")
			validationScores.write("\n------------------------------------------\n")
			
			# Calculating context info for candidate words
			# Calculating context info for candidate words
			for j in range(0,len(CW)):
				Total_Cosine = 0.0
				#context before the inserted word
				if i >= 3:
					Total_Cosine = (compute_score(token[i],CW[j],0) + compute_score(token[i-1],CW[j],1) + compute_score(token[i-2],CW[j],2) + compute_score(token[i-1],token[i],0) + compute_score(token[i-1],token[i+1],2) + compute_score(token[i],token[i+1],1) )/6
				elif i == 2:
					Total_Cosine = (compute_score(token[i],CW[j],0) + compute_score(token[i-1],CW[j],1) + compute_score(token[i-1],token[i],0) + compute_score(token[i-1],token[i+1],2) + compute_score(token[i],token[i+1],1) )/5
				else:
					Total_Cosine = (compute_score(token[i],CW[j],0) + compute_score(token[i],token[i+1],1) + compute_score(token[i],token[i+1],1))/3

				# Context after the inserted word
				if (i+1) <= len(token)-3:
					Total_Cosine = (Total_Cosine + compute_score(CW[j],token[i+1],0) +  compute_score(CW[j],token[i+2],1) + compute_score(CW[j],token[i+3],2) + compute_score(token[i+1],token[i+2],0) + compute_score(token[i+1],token[i+3],1) + compute_score(token[i+2],token[i+3],0))/7
				elif (i+1) == len(token)-2:
					Total_Cosine = (Total_Cosine + compute_score(CW[j],token[i+1],0) + compute_score(CW[j],token[i+2],1) + compute_score(token[i+1],token[i+2],0))/4
				else:
					Total_Cosine = (Total_Cosine + compute_score(CW[j],token[i+1],0))/2

				#Append all the Total Cosine
				CW_Scores.append(Total_Cosine)
				max_i = CW_Scores.index(max(CW_Scores))
				Missing_Word = CW[max_i]

				#Candidate Missing Pair
				CMP[token[i]+","+token[i+1]] = {"MW": Missing_Word, "Score": CW_Scores[max_i]}		
	
	# Compute the maximum missing word score and insert at the location
	maximum = 0.0
	best_key = ""
	missing_word = "_"
	for key in CMP:
		validationScores.write("Pair: " + key + "\n")
		for k in CMP[key]:
			validationScores.write(k + ": " + str(CMP[key][k]) + "\n")
		validationScores.write("******\n\n")
		if maximum < CMP[key]["Score"]:
			best_key = key
			maximum = CMP[key]["Score"]
			missing_word = CMP[key]["MW"]
	validationScores.write("**************************************************************************\n\n")
	

	best_pair = best_key.split(",")
	not_inserted = True
	try:
		index = original.index(best_pair[0])
		original.insert(index+1,missing_word)
		not_inserted = False
	except :
		pass
	if not_inserted:
		try:
			index = original.index(best_pair[1])
			original.insert(index,missing_word)
		except :
			original.insert(0,missing_word)
			pass
	print original
	for word in original:
		word = "".join([ch if ord(ch)<= 128 else "_" for ch in word])
		#word = word.decode('utf-8')
		validationOutput.write(word + " ")
	validationOutput.write("\n")
	validationScores.close()
	validationOutput.close()
