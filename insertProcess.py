import os
import re
from insertNode import insertNode

tokensDict = {}
delTokens = []

def preparationForInsertQuerry():
    global tokensDict, delTokens
    tokensDict = {'into': [], 'cols': [], 'values': []}
    delTokens = ['insert', ';']

def makeListsForNodes(inputString):
    key = None
    for word in inputString:
        if word in tokensDict:
            key = word
        elif word in delTokens:
            continue
        else:
            tokensDict[key].append(word.replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
            if key == 'into':
                key = 'cols'


def insertQ(inputString):
    inputString = inputString['val']
    preparationForInsertQuerry()
    makeListsForNodes(inputString)
    print(tokensDict)
    item = insertNode("insert", tokensDict['into'], tokensDict['cols'], tokensDict['values'])
    item.TransformToNoSQL()
    return item.toString()

