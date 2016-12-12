import pymongo,string,sys
from levenshtein import levenshtein
import numpy as np
from itertools import izip

validationOutput = open(sys.argv[1],'r')
validationGroundTruth = open(sys.argv[2],'r')
missing_word = open(sys.argv[3],'r')

Edit_distance = 0
Accuracy = 0
count = 0
for test_line, groundtruth_line in izip(validationOutput, validationGroundTruth):
	count = count + 1
	test_line = test_line.strip()
	groundtruth_line = groundtruth_line.strip()
	distance = levenshtein(test_line,groundtruth_line)
	Edit_distance = Edit_distance + distance
	if int(distance) == 0:
		Accuracy = Accuracy + 1
	print distance

print "Average Edit Distance: ",Edit_distance/float(count),"Accuracy: ",Accuracy*100/float(count)
word_accuracy = 0
count = 0

for test_line, word_line in izip(validationGroundTruth, missing_word):
	count = count + 1
	test_line = test_line.strip().split(',')
	mword = test_line[1]
	word_line = word_line.strip().split(' ')
	eword = word_line[1]
	print eword,mword
	if mword == eword:
		word_accuracy = word_accuracy + 1

print "Word Accuracy: ",word_accuracy*100/float(count)