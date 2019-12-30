import os
import re
from insertNode import insertNode

tokensDict = {}
delTokens = []

def preparationForInsertQuerry():
    global tokensDict, delTokens
    tokensDict = {'into': [], 'cols': [], 'values': []}
    delTokens = ['insert', ';','(', ',', ' ',')']

def makeListsForNodes(inputString):
    key = None
    theLIST = []
    for word in inputString:
        if word.lower() in tokensDict:
            key = word.lower()
        elif word == ')' and key == 'values':
            tokensDict[key].append(theLIST)
            theLIST = []
        elif word.lower() in delTokens:
            continue
        elif key == 'values':
            theLIST.append(word.replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
        else:
            tokensDict[key].append(word.replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("`", ""))
            if key == 'into':
                key = 'cols'


def insertQ(inputString):
    inputString = inputString['val']
    preparationForInsertQuerry()
    makeListsForNodes(inputString)
    item = insertNode("insert", tokensDict['into'], tokensDict['cols'], tokensDict['values'])
    item.TransformToNoSQL()
    return item.toString()

