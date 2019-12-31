import os
import re
from findNode import findNode
from groupNode import groupNode

tokensDict = {}
delTokens = []
groupTokens = []

def preparationForSelectQuerry():
    global tokensDict, delTokens, groupTokens
    tokensDict = {'select': [], 'from': [], 'where': [], 'order': [], 'group':[]}
    delTokens = ['by', ';']
    groupTokens = ['sum']

def find_between(inputList, first, last):
    try:
        start = inputList.index(first) 
        end = inputList.index(last)
        return inputList[start + 1:end]
    except ValueError:
        return False

def makeListsForNodes(inputString):
    key = None
    for word in inputString:
        if word.lower() in tokensDict:
            key = word.lower()
        elif word.lower() in delTokens:
            continue
        else:
            tokensDict[key].append(word)


def selectQ(inputString):
    preparationForSelectQuerry()
    inputString = inputString['val']
    makeListsForNodes(inputString)
    print('Ana')
    print(tokensDict)
    if len(tokensDict['group']) > 0:
        print("CODREA")
        item = groupNode("group", tokensDict['select'], tokensDict['from'], tokensDict['where'], tokensDict['order'], tokensDict['group'])
    else:
        print("ECHO")
        item = findNode("find", tokensDict['select'], tokensDict['from'], tokensDict['where'], tokensDict['order'])
    item.TransformToNoSQL()

    return item.toString()

_text = re.sub(' +', ' ', "select * from Customers where CustomerName like 'a%'".strip())

_text = _text.replace(';', '')
_text = _text.replace('(', ' ( ')
_text = _text.replace(')', ' ) ')
_text = _text.replace(',', ', ')
_text.lower()
_text = re.sub(' +', ' ', _text.strip())
textList = _text.split()
print("Codrin")
print(textList)
preparationForSelectQuerry()
print('Something about BORDEA')
print(selectQ({'val': textList}))