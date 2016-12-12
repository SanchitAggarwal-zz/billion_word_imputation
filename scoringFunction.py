#Scoring Functions
import math
import numpy

def distanceScore(frequency,window):
	total_freq = 0;
	freq = []
	for i in range(1, window+1):
		if str(i) in frequency:
			value = frequency[str(i)]
			total_freq = total_freq + value
			freq.append(value/float(i))
	freq = numpy.array(freq)
	freq = freq/total_freq
	score = sum(freq)
	return score