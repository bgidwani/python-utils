fhandle = open('<FILE_NAME>')
emptylines = 0
codelines = 0
counts = dict()
for line in fhandle:
    strippedline = line.rstrip()
    if (strippedline == ''):
        emptylines += 1
        continue
    else:
        codelines += 1
    words = strippedline.split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    # print(words)

fhandle.close()
print('# of Empty lines = ' + str(emptylines))
print('# of non Empty lines = ' + str(codelines))
print('Word Histogram', counts)
