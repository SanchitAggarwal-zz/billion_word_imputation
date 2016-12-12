import random, os, string


validationGroundTruth = open('./data/Validation_GroundTruth.txt','r')
validationGroundTruthC = open('./data/Validation_GroundTruthC.txt','a')

start = 1
end = 1000
i = 1
for line in validationGroundTruth:
		line = line.split(",")
		beg = line[0]
		line = line.pop()
		print beg,line
		line = line.translate(string.maketrans("",""), string.punctuation)
		line = line.lower()
		words = line.split()
		if len(words) > 2:
			validationGroundTruthC.write(beg + "," + line)