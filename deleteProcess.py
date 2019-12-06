from deleteNode import deleteNode

tokensDict = {}
delTokens = []

def preparationForDeleteQuerry():
    global tokensDict, delTokens
    tokensDict = {'from': [], 'where': []}
    delTokens = ['delete', ';']

def makeListsForNodes(inputString):
    key = None
    for word in inputString:
        if word in tokensDict:
            key = word
        elif word in delTokens:
            continue
        else:
            tokensDict[key].append(word)

def deleteQ(inputString):
    inputString = inputString['val']
    preparationForDeleteQuerry() 
    makeListsForNodes(inputString)

    item = deleteNode("delete", tokensDict['from'], tokensDict['where'])
    item.TransformToNoSQL()

    return item.toString()
