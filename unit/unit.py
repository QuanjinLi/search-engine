import os
import re
import math
import collections
import json
import time

def createFile(TextFilePath):
    if os.path.exists(TextFilePath):
        #print "File " + TextFilePath + "already exist, please change the name!"
        return -1
    else:
        return open(TextFilePath, 'w+')


def openFile(TextFilePath):
    if os.path.exists(TextFilePath):
        return open(TextFilePath, 'r')
    else:
        #print "File " + TextFilePath + " not exist, please change the name!"
        return -1


def tokenize(TextFilePath):
    #re_word = re.compile(r"[\w']+")
    re_word = re.compile(r"[\w']+")
    file_object = openFile(TextFilePath)
    words = []
    #position = []
    #count = 0
    for line in file_object:
        line = line.replace('\'', '')
        for word in re_word.finditer(line):
            words.append(word.group(0).lower())
            #count += 1
            #position.append(count)
    file_object.close()
    return words


def computerWordFrequencies(Token):
    '''
    Count = {}
    for item in Token:
        if item not in Count:
            Count[item] = 1
        else:
            Count[item] += 1
    '''
    return collections.Counter(Token).items()


def Print(Frequencies):
    #print sortFrequencies(Frequencies)
    return


def sortFrequencies(Frequencies):
    tem = sorted(Frequencies, key=lambda x: (x[0]))
    return sorted(tem, key=lambda x: (x[1]), reverse=True)


def createInput_OutputFile(TextFilePath, list):
    input = createFile(TextFilePath)
    if input == -1:
        return
    else:
        for key, value in list:
            input.write(key + ", " + str(value) + "\n")
        input.close()
        return
