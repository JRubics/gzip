import pickle
import sys
import os
import tarfile
import numpy as np
from pathlib import Path    #za proveru da li postoji ulazni file
from codeDecompress import CodeU
from code import Code

# def countWords(d,dictionary):
#     min = len(dictionary[0].codeStr)
#     for i in range(1,len(dictionary)):
#         if len(dictionary[i].codeStr) < min:
#             min =  len(dictionary[i].codeStr)
#     print(min)
#     for i in range(0,len(dictionary)):
#         for j in range(0,len(d)):
#             for k in range(0,min/2):
#                 k = k
#     return dictionary

def decompressLZ77Codes(d,dictionary,max,unzipFilename):
    s = ''
    i = 0
    # print(len(dictionary))
    decompressed = ''
    while i < len(d):
        a = d[i]
        i += 1
        while d[i] != '=':
            if i == len(d):
                break
            a += d[i]
            i += 1
        # print(a)
        i+=1
        s = ''
        while d[i]!= ';':
            # print(d[i])
            if i == len(d):
                break
            s+=d[i]
            i += 1
        # print(a,s)
        decompressed += translateLZ77(a,s,dictionary)
        i += 1
    return decompressed

def translateLZ77(a,s,dictionary): # W T F
    translated = ''
    for i in range(0,len(dictionary)):
        # print("a = ",a, "  d = ",dictionary[i].binCode)
        if a == dictionary[i].binCode:
            # print(dictionary[i].codeStr)
            for j in range(0,int(s)):
                translated += dictionary[i].codeStr[j]  
    # print(translated)
    return translated

def decompressLZ77dictionary():
    d = readFromFile("dictionary")
    i = 0
    k = 0
    dictionary = []
    while i < len(d):
        a = d[i]
        i += 1
        while d[i] != '=' or (d[i]=='=' and d[i+1] != '0' and d[i+1]!='1'):
            if d[i] == '|':
                break
            a += d[i]
            i += 1
        # print(a)
        # if d[i]=='=' and d[i+1] != '0' and d[i+1]!='1':
        #     # print(d[i+1]);
        #     i += 1
        #     while d[i] != '=':
        #         print(d[i]);
        #         i+=1
        i+=1
        s = ''
        while d[i]!= ',':
            # print(d[i])
            if d[i] == '|':
                break
            s+=d[i]
            i += 1
        c = CodeU(a,s)
        dictionary.append(c)
        i += 1
    return dictionary

def countWords(dd,dictionary): 
    words = makeWords(dd,dictionary)
    for i in range(0,len(words)):
        for j in range(0,len(dictionary)):
            if words[i] == dictionary[j].codeStr[0:len(words[i])]:
                dictionary[j].counter += 1
                break
 
    for j in range(0,len(dictionary)): #zato sto je u startu 1
        dictionary[j].counter -= 1
    return dictionary

def LZ77compress(dd,dictionary):
    words = makeWords(dd,dictionary)
    s = ''
    for i in range(0,len(words)):
        for j in range(0,len(dictionary)):
            if words[i] == dictionary[j].codeStr[0:len(words[i])]:
                s = s + str(bin(dictionary[j].binCode))[2:] + '=' + str(len(words[i])) + ";"
                break
    # print(s)
    return s


def makeWords(dd,dictionary):
    words = []
    d = ''
    for i in range(0,len(dd)):
        d = d + dd[i] # d -> string

    p = dictionary[0].codeStr[0]
    i = 0
    while i < len(d):
        s = 0
        pom = p
        while (d[i+s] != p) and (i+s < len(d)-1):
            pom += d[i+s]
            s += 1
        words.append(pom)
        i += s+1
    del words[0]
    words[len(words)-1] += d[len(d)-1]
    return words

def makeLZ77Dictionary(d): #PROVERI
    dictionary = list()
    found = False
    add = False
    F = d[0]
    dictionary.append(F)
    helpD = [] #ovde se prebaci samo ono sto treba
    # print(len(d))
    for i in range(1,len(d)):
        for s in range(0,len(dictionary)):
            # print("1")
            if dictionary[s][0]== d[i]:
                # print("2")
                F = ''
        pom = F + d[i]
        for j in range(0,len(dictionary)):
            for k in range(0,len(dictionary[j])):
                if pom[k] == dictionary[j][k]:
                    continue
                else:
                    found = True
            if found != True:
                dictionary.append(pom)
                found = False
                F = pom
            break
    for i in range(0,len(dictionary)): #pravi listu za brisanje(zbog onog out of range u for brisanju)
        for j in range(0,len(dictionary)):#proveri sledeci red za len+-1
            if i == j:
                continue
            if len(dictionary[i]) > len(dictionary[j]) and dictionary[i][0:len(dictionary[j])] == dictionary[j]:
                # print(dictionary[j])
                helpD.append(dictionary[j])

    helpD = set(helpD)
    dictionary = [x for x in dictionary if x not in helpD]
    # for i in range(0,len(helpD)): #brisanje
        # while existsInList(helpD[i],dictionary):
        #     print(f'while {a}')
        #     a += 1
        #     dictionary.remove(helpD[i])
    dictionary = set(dictionary)    #unique
    dictionary = list(dictionary)
    return dictionary

def existsInList(x,dictionary):
    # exists = False
    if x in dictionary:
        return True
    else:
        return False
    # for i in range(0,len(dictionary)):
    #     if x == dictionary[i]:
    #         exists = True
    # return exists

def findNextLZ77(d,s,i):
    s = s + d[i]
    print(s)
    for j in range(i+1,len(d)):
        j = j

    return i

def printArray(d):
    for i in range(0,len(d)):
        print(d[i])
    return 0

def decompressHuffmanCodes(d,dictionary,max,filename):
    s = ''
    # printArray(d)
    # printDecompressedDictionary(dictionary)
    for k in range(0,len(d)):
        if d[k] == '0':
            s += d[k]
            translateHuffmanCode(s,dictionary,filename)
            s = ''
        else: #1
            s += d[k]
            if s == max:
                translateHuffmanCode(s,dictionary,filename)
                s = ''
        k += 1
    return 0

def translateHuffmanCode(s,dictionary,filename):
    for i in range(0,len(dictionary)):
        if s == dictionary[i].binCode:
            writeStrToFile(filename,dictionary[i].codeStr)
    return 0

def printDecompressedDictionary(dictionary):
    for i in range(0,len(dictionary)):
        print(dictionary[i].codeStr," code = ",dictionary[i].binCode)        

def decompressDictionary():
    d = readFromFile("dictionary")
    i = 0
    k = 0
    dictionary = []
    for i in range(0,len(d)):
        a = d[i]
        if d[i] == '|':
            break
        if d[i+1] == '=':
            j = i + 2
            s = d[j]
            j += 1
            while d[j] != ',':
                if d[j] == '|':
                    break
                s = s + d[j]
                j += 1
            #print(a," ",s)
            i = j-1
            c = CodeU(a,s)
            dictionary.append(c)
        i += 1
    return dictionary

def emptyDictionaryFile():
    newFile = open("dictionary", "w")
    newFile.close()

def writeDictionaryToFile(dictionary):
    newFile = open("dictionary", "a")
    #
    # pickle.dump(dictionary, open("dictionary", "wb"))

    s = "%s=%s" %(dictionary[0].codeStr, bin(dictionary[0].binCode)[2:])
    newFile.write(s)
    for i in range(1,len(dictionary)):
        newFile.write(',')
        s = "%s=%s" %(dictionary[i].codeStr, bin(dictionary[i].binCode)[2:])
        newFile.write(s)
    newFile.write("|")
    newFile.close()
    return 0

def writeCodeToFile(filename,s):
    newFile = open(filename, "w")
    newFile.write(s)
    newFile.close()
    return 0

def writeStrToFile(filename,s):
    newFile = open(filename, "a")
    newFile.write(s)
    newFile.close()
    return 0

def arrayToStr(gzip):
    s = bin(gzip[0])[2:]
    for i in range(1,len(gzip)):
        p = s
        s = "%s%s" %(p,bin(gzip[i])[2:])
    return s

def printArrayFromFile(filename):
    d = readFromFile(filename)
    for i in range(0,len(d)):
        print(d[i])
    return 0

def huffmanCompression(dicionary,d):
    gzip = []
    for i in range(0,len(d)):
        for j in range(0,len(dicionary)):
            if d[i] == dicionary[j].codeStr:
                gzip.append(dicionary[j].binCode)
                #print(bin(gzip[i]))
    return gzip

def makeHuffmanCodes(dictionary):
    dictionary[0].binCode = 0b0
    dictionary[1].binCode = 0b10
    k = 2
    shiftAndAdd(dictionary,k)
    return 0

def shiftAndAdd(dictionary,k):
    if k+1 == len(dictionary):
        dictionary[k].binCode = dictionary[k-2].binCode * 2 + 3
        return 0
    dictionary[k].binCode = dictionary[k-1].binCode * 2 + 2
    shiftAndAdd(dictionary,k+1)
    return 0

def printDictionary(dictionary):
    for i in range(0,len(dictionary)):
        print(dictionary[i].codeStr," c = ",dictionary[i].counter," code = ",bin(dictionary[i].binCode))
    return 0

def sortDictionary(dictionary):
    for i in range(0,len(dictionary)-1):
        for j in range(i,len(dictionary)):
            if dictionary[i].counter < dictionary[j].counter:
                temp = dictionary[i].counter
                dictionary[i].counter = dictionary[j].counter
                dictionary[j].counter = temp
                temp = dictionary[i].binCode
                dictionary[i].binCode = dictionary[j].binCode
                dictionary[j].binCode = temp
                temp = dictionary[i].codeStr
                dictionary[i].codeStr = dictionary[j].codeStr
                dictionary[j].codeStr = temp

    for d in range(1,dictionary[0].counter+1):
        for i in range(0,len(dictionary)-1):
            if dictionary[i].counter == d:
                for j in range(i,len(dictionary)):
                    if len(dictionary[i].codeStr) < len(dictionary[j].codeStr) and dictionary[j].counter == d:
                        temp = dictionary[i].counter
                        dictionary[i].counter = dictionary[j].counter
                        dictionary[j].counter = temp
                        temp = dictionary[i].binCode
                        dictionary[i].binCode = dictionary[j].binCode
                        dictionary[j].binCode = temp
                        temp = dictionary[i].codeStr
                        dictionary[i].codeStr = dictionary[j].codeStr
                        dictionary[j].codeStr = temp
    return 0

def makeDictionary(inputStr):
    dictionary = []
    found = []
    c = Code(inputStr[0],1,0)
    dictionary.append(c)
    found.append(inputStr[0])
    for i in range(1,len(inputStr)):
        if inputStr[i] in found:
            for j in range(0,len(dictionary)):
                if dictionary[j].codeStr == inputStr[i]:
                    dictionary[j].counter += 1
        else:
            c = Code(inputStr[i],1,0)
            dictionary.append(c)
            found.append(inputStr[i])
    return dictionary

def readZip(filename):
    i = 0
    readList = []
    newlist = []
    my_file = Path(filename)
    a = ''
    if my_file.is_file():
        try: 
            with open(filename) as f:
                while True:
                    c = f.read(1)
                    if not c:
                        break
                    readList.append(c)
        finally:
            f.close()
    else:
        print("Can not open a file")
        exit(0)
    # for i in range (0,len(readList)):
    #     # print(readList[i])
    #     if (readList[i] == 'b' and readList[i+1] == '\'') or (readList[i-1] == 'b' and readList[i] == '\''):
    #         continue
    #     if (readList[i] == '\'' and readList[i+1] == '='):
    #         continue
    #     if(readList[i-1] == '\'' and readList[i] == '='):
    #         newlist.append('=')
    #         continue
    #     else:
    #         newlist.append(readList[i])
    return newlist

def readFromFile(filename):
    i = 0
    readList = []
    my_file = Path(filename)
    a = ''
    if my_file.is_file():
        try: 
            # with open(filename) as f:
            #     while True:
            #         c = f.read(1)
            #         if not c:
            #             break
            #         readList.append(c)

            with open(filename, mode='rb') as file:
                a = file.read()
                file.close()
                # print(a)
            string = a.decode('utf-8')
            # print(string)

        finally:
            # f.close()
            for i in range(0,len(string)):
                readList.append(string[i])
            # print(readList)
            return readList
    else:
        print("Can not open a file")
        exit(0)

# def writeArrayToFile(filename,inputStr):
#     inputStr = np.array(inputStr)
#     newFile = open(filename, "wb")
#     newFile.write(inputStr)
#     return 0

 # with open(filename, mode='rb') as file: # b is important -> binary
            #     a = file.read()
            #     file.close()
            # print(a)
            # f = open(filename, "rb")
            # byte = f.read(1)
            # while byte != b"":
            #     #print(byte)
            #     readList.append(byte)
            #     byte = f.read(1)
