def viterbi(sentence, emission, transition):
    sentencePos = ["START"]
    maxp = -1
    currentPos = "START"
    helper = {}
    # print(helper)
    for x in transition:
        helper[x] = {}
        for y in sentence:
            helper[x][y] = 0
    for i in range(len(sentence) - 1):
        currentWord = sentence[i]
        # print("currentWord",currentWord)
        if (i == 0):
            nextWord = sentence[i + 1]
            # print("nextWord",nextWord)
            for pos in transition:
                if (pos == "START"):
                    pass
                else:
                    t = transition[currentPos][pos]
                    if nextWord in emission:
                        e = emission[nextWord][pos]
                    else:
                        e = 1 / (len(transition) - 1)
                    p = t * e
                    helper[pos][nextWord] = p
        else:
            nextWord = sentence[i + 1]

            # print("nextWord",nextWord)
            for thispos in transition:
                if (thispos == "START"):
                    pass
                else:
                    if nextWord in emission:
                        e = emission[nextWord][thispos]
                    else:
                        e = 1 / (len(transition) - 1)
                    maxp = -1
                    for prepos in transition:

                        if (thispos == "START"):
                            pass
                        else:

                            t = transition[prepos][thispos]
                            h = helper[prepos][currentWord]
                            p = t * e * h
                            if (p > maxp):
                                maxp = p
                    helper[thispos][nextWord] = maxp
    # print(helper)
    maxProb = []
    for x in sentence:
        maxp = -1
        pos = ""
        for y in helper:
            p = helper[y][x]
            if (p > maxp):
                maxp = p
                pos = y
        maxProb.append(pos)

    return maxProb


def readFile(keyFileName):


    pos = []
    poslist = []
    dict = {}
    keyFile = open(keyFileName, 'r')
    key = keyFile.readlines()
    keyPos = ["START"]
    keyWord = [""]

# x=keyPos[0]
# if x not in poslist:
#     poslist.append(x)

    for i in range(len(key)):
        key[i] = key[i].rstrip('\n').strip()
        if key[i] == "":
            keyWord.append("")
            keyPos.append("END")

            # x="END"
            # if x not in poslist:
            #     poslist.append(x)

            keyWord.append("")
            keyPos.append("START")
            continue
        else:
            keyFields = key[i].split('\t')
            keyWord.append(keyFields[0])
            keyPos.append(keyFields[1])
            # x=keyFields[1]
            # if x not in poslist:
            #     poslist.append(x)
    keyWord.append("")
    keyPos.append("END")
    return keyWord, keyPos



trainFileName = "POS_CORPUS_FOR_STUDENTS/POS_train.pos"
devFileName = "POS_CORPUS_FOR_STUDENTS/POS_dev.pos"

keyWord1,keyPos1 = readFile(trainFileName)
keyWord2,keyPos2 = readFile(devFileName)

keyWord = keyWord1 + keyWord2
keyPos = keyPos1 + keyPos2
# for i in range(len(keyWord)):
#     print (keyWord[i], "\t", keyPos[i])

# intilize a null list
poslist = []
wordlist = []
# traverse for all elements
i = 0
transition = {}
emission = {}
for x in keyPos:
    # check if exists in unique_list or not
    if x not in poslist:
        poslist.append(x)

for x in keyWord:
    # check if exists in unique_list or not
    if x not in wordlist:
        wordlist.append(x)

for x in poslist:
    transition[x] = {}
    transition[x]['appered'] = 0
    for y in poslist:
        transition[x][y] = 0


for x in wordlist:
    emission[x] = {}
    for y in poslist:
        emission[x][y] = 0
# for x in dict:
#     print (dict[x])
i = 0
for i in range(len(keyPos)):
    if keyPos[i] != "END":
        first = keyPos[i]
        second = keyPos[i + 1]
        a = transition[first][second]
        a = a + 1
        transition[first][second] = a
    first = keyPos[i]
    b = transition[first]['appered']
    b = b + 1
    transition[first]['appered'] = b

i = 0
for i in range(len(keyWord)):
    if keyPos[i] != "END":
        word = keyWord[i]
        pos = keyPos[i]
        a = emission[word][pos]
        a = a + 1
        emission[word][pos] = a

# for x in transition:
#     print (x)
#     print (transition[x])
# for x in emission:
#     print (x)
#     print (emission[x])


transition1 = {}
emission1 = {}

for x in poslist:
    transition1[x] = {}
    for y in poslist:
        transition1[x][y] = 0

for x in wordlist:
    emission1[x] = {}
    for y in poslist:
        emission1[x][y] = 0

for x in transition:
    for y in transition[x]:
        a = transition[x][y]
        b = transition[x]['appered']
        transition1[x][y] = a / b

for x in emission:
    for y in emission[x]:
        a = emission[x][y]
        b = transition[y]['appered']
        emission1[x][y] = a / b

del transition1["END"]
for x in transition1:
    del transition1[x]['appered']
    del transition1[x]["START"]


##############################
# VITERBI DECODING
##############################

pos = []

poslist = []
dict = {}
keyFileName = "POS_CORPUS_FOR_STUDENTS/POS_test.words"
keyFile = open(keyFileName, 'r')
key = keyFile.readlines()
keyWord = ["START"]

# x=keyPos[0]
# if x not in poslist:
#     poslist.append(x)

for i in range(len(key)):
    key[i] = key[i].rstrip('\n').strip()
    if key[i] == "":
        keyWord.append("END")

        # x="END"
        # if x not in poslist:
        #     poslist.append(x)

        keyWord.append("START")
        continue
    else:
        keyWord.append(key[i])
        # x=keyFields[1]
        # if x not in poslist:
        #     poslist.append(x)
keyWord.append("END")

sentence = []
sentencePos = []
keyPos = []
for x in keyWord:
    if (x != "END"):
        sentence.append(x)
    else:
        sentence.append(x)
        sentencePos = viterbi(sentence, emission1, transition1)
        # print(sentence)
        # print(sentencePos)
        keyPos = keyPos + sentencePos
        sentence = []

outF = open("POS_CORPUS_FOR_STUDENTS/POS_testOutput.pos", "w")

# print (keyWord)
# print (keyPos)
# print (len(keyWord))
# print (len(keyPos))
for i in range(len(keyWord)):
    # write line to output file
    word = keyWord[i]
    pos = keyPos[i]
    line = str(word) + "\t" + str(pos)
    if (word == "START"):
        pass
    elif (word == "END"):
        if (i==(len(keyWord)-1)):
            pass
        else:
            outF.write("\n")
    else:
        outF.write(line)
        outF.write("\n")
outF.close()
# for x in keyPos:
#     print(x)
