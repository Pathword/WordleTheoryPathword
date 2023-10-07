import itertools
import random 
from collections import Counter

####################################################################

"""
IMPORT
"""

AllWordsLaPath = "C:\\Users\\Dylan\\MyPython\\MyProjects\\Wordle\\Resources\\wordle-La.txt"
AllWordsTaPath = "C:\\Users\\Dylan\\MyPython\\MyProjects\\Wordle\\Resources\\wordle-Ta.txt"

try: 
    with open(AllWordsLaPath, 'r') as file:
        AllWordsLaRaw = file.read()
        AllWordsLa = AllWordsLaRaw.split("\n")

except FileNotFoundError:
    print(AllWordsLaPath + " not found")


try: 
    with open(AllWordsTaPath, 'r') as file:
        AllWordsTaRaw = file.read()
        AllWordsTa = AllWordsTaRaw.split("\n")

except FileNotFoundError:
    print(AllWordsTaPath + " not found")


####################################################################

"""
THEORY
"""
def FindMostCommonLetters(AllWordsLa):
    AllLetters = "qwertyuiopasdfghjklzxcvbnm"
    LetterFreq = {}

    #letter frequency in all possible answers
    for Word in AllWordsLa:
        for n in Word:
            if n in LetterFreq.keys():
                LetterFreq[n] += 1
            else:
                LetterFreq[n] = 1

    #easy to view most common letters, not necessary
    sorted_data = dict(sorted(LetterFreq.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_data

#Trying to figure out best possible first word based on all possible answers
#wordle-La is all possible ANSWERS while wordle-Ta is all possible GUESSES
def FindBestWords(AllWordsTa,Letters):
    
    words_list = [''.join(word) for word in itertools.permutations(Letters, 5)]

    BestWords = []

    for n in words_list:
        if n in AllWordsTa:
            BestWords.append(n)

    return BestWords

#return dict of top five
def GetTopFive(LetterFreq):
    TopFive = {}

    for n in range(0,5):
        key = list(LetterFreq.keys())[n]
        value = list(LetterFreq.values())[n]
        
        TopFive[key] = value
    
    return TopFive

def GetGreenConfirms(AllWordsLa,Guess):

    confirms = {}

    for n in Guess:
        confirms[n] = 0

    for word in AllWordsLa:
        for n in range(0,5):
            if Guess[n] == word[n]:
                confirms[Guess[n]] +=1

    TotalConfirms = sum(list(confirms.values()))
    return confirms, TotalConfirms




LetterFreq = FindMostCommonLetters(AllWordsLa)
TopFiveFreq = GetTopFive(LetterFreq)
BestWords = FindBestWords(AllWordsTa,"earot")
print(BestWords)
#ROATE is best first guess based on most common letters, AND most green hits


#not doing excess coding... its been determined "earot" is most common letters
#['roate', 'oater', 'orate'] best first words
#however can "blackout on" earot, filter AllWordsLa and sort by letter freq again

#get rid of all words containing earot, "blackout" scenario 
AllWordsMinusEAROT = []
MostCommon = "earot"

for word in AllWordsLa:
    c = 0 
    for n in MostCommon:
        if n in word:
            c+=1

    if c==0:
        AllWordsMinusEAROT.append(word)

#get letter freq of allwordsminusearot

LetterFreq = FindMostCommonLetters(AllWordsMinusEAROT)
TopFiveFreq = GetTopFive(LetterFreq)

asdf = "uilsc"

BestWords = FindBestWords(AllWordsTa,asdf)

#none... best SEEMS to be lysin
#search AllWordsMinusEarot

WordsNotinasdf = []
for word in AllWordsMinusEAROT:
    c = 0 
    for n in asdf:
        if n in word:
            c+=1
    if c==0:
        WordsNotinasdf.append(word)

#best word 
print(BestWords)
print(WordsNotinasdf)
