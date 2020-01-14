import os
import re
from findNode import findNode
from groupNode import groupNode
from joinNode import joinNode

tokensDict = {}
delTokens = []
groupTokens = []

def preparationForSelectQuerry():
    global tokensDict, delTokens, groupTokens
    tokensDict = {'select': [], 'from': [], 'where': [], 'order': [], 'group':[], 'inner':[], 'on':[], 'using':[], 'as':[], 'limit': []}
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
        elif word.lower() == 'join':
            key = 'inner'
        elif word.lower() in delTokens:
            continue
        else:
            tokensDict[key].append(word)
    
    if len(tokensDict['from']) > 1:
        for item in tokensDict['from'][1:]:
            tokensDict['inner'] = [item]
        tokensDict['from'] = [tokensDict['from'][0]]



def selectQ(inputString):
    preparationForSelectQuerry()
    inputString = inputString['val']
    makeListsForNodes(inputString)

    if len(tokensDict['inner']) > 0:
        item = joinNode("group", tokensDict['select'], tokensDict['from'], tokensDict['where'], tokensDict['order'], tokensDict['inner'], tokensDict['on'], tokensDict['using'], tokensDict['as'], tokensDict['limit'], tokensDict['group'])
    elif len(tokensDict['group']) > 0:
        item = groupNode("group", tokensDict['select'], tokensDict['from'], tokensDict['where'], tokensDict['order'], tokensDict['group'], tokensDict['limit'])
    else:
        item = findNode("find", tokensDict['select'], tokensDict['from'], tokensDict['where'], tokensDict['order'], tokensDict['limit'])
    item.TransformToNoSQL()

    return item.toString()

