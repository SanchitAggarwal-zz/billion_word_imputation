
line="Hi I am ajeet"

l = word_tokenize(line)
print l

d = ngrams(l, 2)

for i in d:
	firstword=i[0]
	first = ht.tag(word_tokenize(firstword))
	secondword=i[1]
	second = ht.tag(word_tokenize(secondword))
	print first, second