

def readFile():
    #print('readFile')
    scorelist = []
    try:
        fileObject = open('.score', 'r')
    except:
        return []
    scoreString = fileObject.read()
    #print('hello')
    #print(scoreString)
    stringList = scoreString.split(';')
    #print(stringList)
    for s in stringList:
        try :
            s = s.strip('\n')
            #print(int(s))
            scorelist.append(int(s))
        except:
            #print("unvalid string", s)
            continue
    scorelist.sort()
    scorelist.reverse()
    #print(scorelist)
    fileObject.close()
    return scorelist



def writeFile(scorelist):
    #print("writeFile")
    try:
        fileObject = open('.score','w')
    except:
        print("ERROR: could not open file")
        return
    scorelist.sort()
    scorelist.reverse()
    for score in scorelist:
        #print(score)
        scoreString = str(score) + ";"
        #print(scoreString)
        fileObject.write(scoreString)
    fileObject.close()




def testDriver():
    scorelist = readFile()
    scorelist.append(1400)
    writeFile(scorelist)
    print(scorelist)


#testDriver()
