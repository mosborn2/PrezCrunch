#For CS491 Let's parse candidate debates
#By Morgan Osborn
#f: this py will parse the text into parts of speech and then produce JSON based on LIWC word usage

#NOTE: We are not statisticians!! This is hardly a rigorous application of LIWC concepts

import json
from textblob import TextBlob


def candText(candname):
    with open("resourcetxt.txt", 'r') as r:
        filenames = r.readlines()
        candtxt = ""
        for fn in filenames:
            with open(fn.strip(), 'r') as f:
                txt = f.read()
                sptxt = txt.split()
                can = False
                for word in sptxt:
                    if word == candname:
                        can = True
                        continue
                    elif str.isupper(word.replace(':', 'A')):
                        can = False
                    if can is True:
                        candtxt += word + " "

        with open(candname.replace(':', ".txt") , 'w') as n:
            n.write(candtxt) 
                
def candSet(candname):
    with open(candname.strip(), 'r') as f:
        txt = f.read()
        t = TextBlob(txt)
        toktxt = t.words
        wordnum = len(toktxt)
        toksent = t.sentences
        sentnum = len(toksent)

        sixcnt = 0
        singcnt = 0
        sentcnt = 0

        solocnt = 0
        for w in [ 'I', 'me', 'mine', 'my' ]:
            solocnt += t.word_counts[w]

        socicnt = 0
        for w in ['they', 'them', 'their', 'themselves' ]:
            socicnt += t.word_counts[w]

        for word in toktxt:
            if len(word) > 5:
                sixcnt += 1

        return { "name" : candname.replace(".txt", "").capitalize(),
               "self" : format(solocnt/wordnum, '.3f'), 
               "formal" : format( sixcnt/wordnum, '.3f'), 
               "complex" : format(wordnum/sentnum, '.3f'), 
               "social" : format(socicnt/wordnum, '.3f') }




def genData():
    candlist = []

    with open("cands.txt", 'r') as r:
        filenames = r.readlines()
        for fn in filenames:
            cSet = candSet(fn.strip())
            candlist.append(cSet)


    with open("candData.json", 'w') as f:
        json.dump(candlist, f)
    print (candlist)

#provide names in allcaps based on input text format
for name in {"TRUMP", "CLINTON", "SANDERS", "CRUZ"}:
    candText(name)
genData()
