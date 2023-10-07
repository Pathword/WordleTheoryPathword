import itertools
import random 
import pyperclip
import json
import time
from collections import Counter

####################################################################

"""
IMPORT
"""

AllWordsLaPath = "C:\\Users\\Dylan\\MyPython\\MyProjects\\Wordle\\Resources\\wordle-La.txt"
AllWordsTaPath = "C:\\Users\\Dylan\\MyPython\\MyProjects\\Wordle\\Resources\\wordle-Ta.txt"
DataExportPath = "C:\\Users\\Dylan\\MyPython\\MyProjects\\Wordle\\Data"

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



"""
allGreenConfirms = []
AllWords = AllWordsLa + AllWordsTa
for word in AllWords:
    allGreenConfirms.append([word,GetGreenConfirms(AllWordsLa,word)])

asdf = []
for n in range(len(allGreenConfirms)):
    if allGreenConfirms[n][1][1] == 1575:
        print(allGreenConfirms[n])
    asdf.append(allGreenConfirms[n][1][1])
"""
####################################################################
"""
TOOLS
RemoveLettersFromCW(WorkingWords,L)

"""

#TOOL RemoveLetterFromCW, removes all words CONTAINING blacks, asdfg. 
#guess roate returned all black, remove all words in the current working words (CW) that contain r, o, a, t, e
#guess roate returned 3 blacks, r, o, a. remove all words in the CW that contain r, o, a

#blacks, remove words containing blacks
def RemoveLettersFromCW(CW,CGStatus):
    
    Letters = CGStatus[0]
    guess = "".join(Letters)
    Status = CGStatus[1]
    
    Greens = {}
    for n in range(0,5):
        if Status[n] == "gr":
            Greens[Letters[n]] = n

    NewWorkingWords = []
    for word in CW:
        #have to add counter to make sure each conditional is met for the word
        c = 0 
        for n in range(0,5):
            #if status is black and not in a greens, 
            if (Status[n] == "bl") and (Letters[n] not in Greens.keys()):
                #Letter in word, DONT add 
                if Letters[n] in word:
                    c+=1
                    
                
                        
            #elif Letter is status black AND is in Greens, splice at index and check if letter in new modified word
            #example, answer = "probe" guess = "saree", CGStatus returns ['bl', 'bl', 'yl', 'bl', 'gr']
            #Greens = {'e' = 4}

            elif (Status[n] == "bl") and (Letters[n] in Greens.keys()):
                ModifiedWord = word
                #? might be able to have multiple blacks on 1 green, future proofing... 
                for key,value in Greens.items(): 
                    if Status[value] == "bl":
                        #have to make sure the marked green is in the correct position on the word
                        if word[value] == key:
                            
                            #splice word at value that has green 
                            ModifiedWord = ModifiedWord[:value] + ModifiedWord[value+1:]

                            #if letter marked black BUT has green is in modified word, word is NOT ACCEPTABLE
                            if (Letters[n] in ModifiedWord):
                                c+=1
                            
                         

        #if c!=0, conditions met
        if c == 0:
            #if word not currently in NewWorkingWords
            if word not in NewWorkingWords:
                NewWorkingWords.append(word)
                    
                    #cut word at indexed 

    """
    NewWorkingWords =[]
    for word in CW:
        for n in range(0,5):
            
            if (Status[n] == "bl") and (Letters[n] not in Greens):
                if (Letters[n] not in word) and (word not in NewWorkingWords):
                    NewWorkingWords.append(word)
    """

    #same word will hit for some reason if green exists.. remove guessed word
    if guess in NewWorkingWords: 
        NewWorkingWords.remove(guess)

    return NewWorkingWords

#RemoveLetters from current working words that DO NOT contain green confirms (GC) at position
#green hits, remove words that DO NOT contain letter at exact position, must be list. 
#"CGStatus" type list, example: 
#answer = "renew"
#guess = "roate"
#output = ['gr', 'bl', 'bl', 'bl', 'yl']
#therefore GreensPosition = ["r",0,0,0,0]
#remove all words that do not contain "r" at position 0 in CGStatus

#greens, remove words that dont have greens at position 
def RemoveLetters_GC_FromCW(CW,CGStatus):
    Letters = CGStatus[0]
    Status = CGStatus[1]
    GreensPosition = []

    for n in range(0,5):
        if Status[n] == "gr":
            GreensPosition.append(Letters[n])
        else:
            GreensPosition.append(0)

    numberOfGreens = 5 - GreensPosition.count(0)

    NewWorkingWords = []
    #if word contains letter at position, append
    for word in CW:
    
        c=0
        for n in range(0,5):
            if GreensPosition[n] != 0:
                if GreensPosition[n] == word[n]:
                    c+=1
        if c==numberOfGreens:
            if word not in NewWorkingWords:
                    NewWorkingWords.append(word)

    return NewWorkingWords

def RemoveLetters_YC_FromCW(CW,CGStatus):
    Letters = CGStatus[0]
    Status = CGStatus[1]
    YellowsPosition = []
    AllYellowLetters = ""

    for n in range(0,5):
        if Status[n] == "yl":
            YellowsPosition.append(Letters[n])
            AllYellowLetters += Letters[n]
        else:
            YellowsPosition.append(0)

    AllYellowLettersCount = len(AllYellowLetters)

    def YellowInWord(word,YellowPosition,n):
        if YellowsPosition[n] != 0: 
            if YellowsPosition[n] != word[n]:
                if YellowsPosition[n] in word:
                    return True
                else:
                    return False
                    
    #if word contains letter at position, GET RID OF 
    NewWorkingWords = []
    for word in CW:
        for n in range(0,5):
            if YellowInWord(word,YellowsPosition,n):

                RangeExcluding_n = list(range(0,5))
                RangeExcluding_n.remove(n)
                #iterate over all other letters, if yellow check same conditions
                c = 0
                for j in RangeExcluding_n:
                    if YellowInWord(word,YellowsPosition,j):
                                c+=1
                if c == AllYellowLettersCount-1:
                    if word not in NewWorkingWords:
                        NewWorkingWords.append(word)

    
    return NewWorkingWords


"""
THEORIES

"""
####################################################################

#Theory 0, pick word at random
def GetRandomWord(CW):
    return CW[random.randint(0,len(CW)-1)]
    

#Theory 1, get green confirms 
def GreenConfirms(CW):

    def GetGreenConfirms(AllWordsLa,guess):

        confirms = {}

        for n in guess:
            confirms[n] = 0

        for word in AllWordsLa:
            for n in range(0,5):
                if guess[n] == word[n]:
                    confirms[guess[n]] +=1

        TotalConfirms = sum(list(confirms.values()))
        return guess, TotalConfirms, confirms

    GreenConfirms = {}
    #compare each word against all other words, create dict of key word with values # of green hits
    for n in range(len(CW)):
        word = CW[n]
        #dont want to compare word against itself... "aback" compared to "aback" gives 5 greens
        CWMinusWord = CW[:n] + CW[n+1:]
        GreenConfirms[word] = GetGreenConfirms(CWMinusWord,word)[1]

    #grab word with max greens
    #NEW GUESS CAN BE SAME AS OLD, 
    NewGuess = max(GreenConfirms,key=lambda k:GreenConfirms[k])

    return NewGuess

#Theory 2, get most matching letters, will double count "aback" will count occurences of "a" twice 
def FindMostMatchingLetters(CW):
    LettersCount = {}
    #get LettersCount
    CWjoined = "".join(CW)

    for letter in CWjoined:
        if letter in LettersCount:
            LettersCount[letter] += 1
        else:
            LettersCount[letter] = 1

    AllWordsLetterCount = {}
    WordLetterCount = 0
    #entries will double count, no worries. each entry should count itself... 
    for word in CW:
        WordLetterCount = 0
        for n in range(0,5):
            #letters will double count, "aback", a will be counted twice... could give different results 
            WordLetterCount += LettersCount[word[n]]
        
        AllWordsLetterCount[word] = WordLetterCount
    
    NewGuess = max(AllWordsLetterCount,key=lambda k:AllWordsLetterCount[k])
    return NewGuess


    
#Theory 3, get most UNIQUE letters, will not double count "aback", only will count "abck"
def FindMostUniqueMatchingLetters(CW):
    
    return True

####################################################################

#PLAYER

def processGuess(answer,guess):
    working = [list(guess),[0,0,0,0,0]]

    LetterCountInAns = dict(Counter(list(answer)))


    for n in range(0,5):
        #black cond
        if guess[n] not in answer:
            working[1][n] = "bl"
        
        #green cond
        if guess[n] == answer[n]:
            working[1][n] = "gr"
            LetterCountInAns[guess[n]] = LetterCountInAns[guess[n]] - 1


    for n in range(0,5):
        #yellow cond
        if (guess[n] in answer) and (guess[n] != answer[n]) and (LetterCountInAns[guess[n]] > 0):
            working[1][n] = "yl"
        elif working[1][n] != "gr":
            working[1][n] = "bl"


    solved = 0 
    for n in working[1]:
        if n == "gr":
            solved+=1

    CGStatus = [working[0],working[1],solved]
    return CGStatus

#CG = "asdfg"
#status = 01201 
#0 = black, 1 = yellow, 2 = green
def ManualCGStatus(CG,status):
    CGStatus = [list(CG)]
    
    status = [int(n) for n in status]
    statusList = []
    for n in status:
        if n == 0:
            statusList.append("bl")
        if n == 1:
            statusList.append("yl")
        if n == 2:
            statusList.append("gr")

    CGStatus.append(statusList)
    return CGStatus

#remove words based on CGStatus, create new CW 
def FilterWordsFromCGStatus(CW,CGStatus):
    #blacks, remove words containing flagged blacks 
    if "bl" in CGStatus[1]:
        CW = RemoveLettersFromCW(CW,CGStatus)

    #check for greens
    if "gr" in CGStatus[1]:
        #greens, remove words NOT containing flagged greens at position
        CW = RemoveLetters_GC_FromCW(CW,CGStatus)
    
    #check for yellows
    if "yl" in CGStatus[1]:
        #yellows, removes words that contain letter at position, BUT have letter in word 
        CW = RemoveLetters_YC_FromCW(CW,CGStatus)
    
    return CW



#CGStatus = ["letters","positionStatus",solves]
#CGStatus = [['b', 'i', 'r', 't', 'h'],['gr', 'bl', 'yl', 'gr', 'gr'],3]
####################################################################

#PLAYING
def FilterWords(answer,guess,CW):
    CGStatus = processGuess(answer,guess)
    #filter greens, blacks, yellows
    CW = FilterWordsFromCGStatus(CW,CGStatus)
    """
    PICK NEW WORD ??? THEORY 
    """

    return CW



#solve from known answer
def SolveWordle(answer,FirstGuess,AllWordsLa,theory):
    #if you got it first try, cool beans. 1 attempt 
    if answer != FirstGuess:
        solved = 0
    else:
        attempts = 1
        return FirstGuess, attempts
    
    CGStatus = processGuess(answer,FirstGuess)
    CW = AllWordsLa
    
    #inputing first guess is 1 attempt, start on 1 attempt 
    attempts = 1

    #can possibly guess right on first attempt
    while True:
        if (CGStatus[2] == 5) or attempts > 100:
            break
        
        #filter words 
        CW = FilterWordsFromCGStatus(CW,CGStatus)

        #PICK NEW WORD!!! Theory...
        #theory 0, pick random word from CW 
        if theory == 0:
            guess = GetRandomWord(CW)
            CGStatus = processGuess(answer,guess)
            attempts += 1

        #theory 1, pick word that provides MOST GREEN CONFIRMS among all possible words (CW)
        #THEORY: 
        if theory == 1:
            if attempts == 1:
                c= 0
                for x in CGStatus[1]:
                    if x =="bl":
                        c+=1
                
                if c ==5:
                    guess = "courd"
                    CGStatus = processGuess(answer,guess)
                else:
                    guess = GreenConfirms(CW)
                    CGStatus = processGuess(answer,guess)
            else:
                guess = GreenConfirms(CW)
                CGStatus = processGuess(answer,guess)
            """
            #Most Green Confirms theory 
            guess = GreenConfirms(CW)
            CGStatus = processGuess(answer,guess)
            """
            attempts += 1

        if theory == 2:
            if attempts == 1:
                c= 0
                for x in CGStatus[1]:
                    if x =="bl":
                        c+=1
                
                if c ==6:
                    guess = "courd"
                    CGStatus = processGuess(answer,guess)
                else:
                    guess = FindMostMatchingLetters(CW)
                    CGStatus = processGuess(answer,guess)
            else:
                guess = FindMostMatchingLetters(CW)
                CGStatus = processGuess(answer,guess)
            """
            #Most Matching Letters Theory
            guess = FindMostMatchingLetters(CW)
            CGStatus = processGuess(answer,guess)
            """
            attempts += 1

    return guess, attempts 
"""
guess = "saree"
#generate random answer
answer = AllWordsLa[random.randint(0,len(AllWordsLa)-1)]

result, attempts = SolveWordle(answer,guess,AllWordsLa,1)
print(result)
print(attempts)
"""




#THEORIES:
#0 choose next word at random
#1 choose next word that provides most green hits 
#analyse first guess on all possible words in La based on theory
#saves file with answer and corresponding # of guesses
#prints attempts per solve to terminal 
def Analysis(guess,Theory,AllWordsLa,DataExportPath):
    if (guess not in AllWordsTa) and (guess not in AllWordsLa):
        print("guess not acceptable")
        return 0

    Theories = ["RAND","MG","MY"]
    
    #run intial guess on ALL possible answers in AllWordsLa
    results = {}    
    for answer in AllWordsLa:
        result, attempts = SolveWordle(answer,guess,AllWordsLa,1)
        print(answer,result,attempts)
        results[result] = attempts

    SortedResults = dict(sorted(results.items(), key=lambda item: item[1]))

    TotalAttempts = 0
    for key, value in SortedResults.items():
        TotalAttempts += value

    AttemptsPerSolve = TotalAttempts/len(SortedResults)
    print(guess)
    print(str(AttemptsPerSolve))

    #save guess data 
    try: 
        with open(DataExportPath + "\\" +str(guess) + "_" +Theories[Theory] +".txt", 'w') as file:
            file.write(Theories[Theory] + "\n")
            file.write("AttemptsPerSolve: " + str(AttemptsPerSolve) +"\n")
            json.dump(SortedResults,file,indent = 4)

    except FileNotFoundError:
        print(DataExportPath + "\\" +str(guess) +Theories[Theory] +".txt" + " not found")


start = time.time()
guess = "salet"
#Run analysis, input guess, theory, dataexport path 
Analysis(guess,1,AllWordsLa,DataExportPath)
end = time.time()

print(end-start)

#CGStatus = ManualCGStatus("roate","01000")
#CW = FilterWordsFromCGStatus(CW,CGStatus)





