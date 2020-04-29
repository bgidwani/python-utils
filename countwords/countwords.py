fhandle = open('<FILE_NAME>')
emptylines = 0
codelines = 0
wordcount = 0
counts = dict()
maxOccur = ('', 0)
for line in fhandle:
    strippedline = line.rstrip()
    if (strippedline == ''):
        emptylines += 1
        continue
    else:
        codelines += 1
    words = strippedline.split()
    wordcount += len(words)
    for word in words:
        counts[word] = counts.get(word, 0) + 1
        if (counts[word] > maxOccur[1]):
            maxOccur = (word, counts[word])
    # print(words)

fhandle.close()


print('# of Empty lines = ' + str(emptylines))
print('# of non Empty lines = ' + str(codelines))
print('# of words = ' + str(wordcount))
print('Max occurring word = ',  maxOccur)
#print('Word Histogram', counts)
