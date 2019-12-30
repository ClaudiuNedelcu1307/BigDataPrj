from createNode import createNode

delTokens = ['create', ';','(', ',', ' ',')', 'table', 'if', 'not', 'exists']

def makeListsForNodes(inputString):
    for word in inputString:
        if word.lower() in delTokens:
            continue
        else:
            return word.replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("`", "")

def createQ(inputString):
    inputString = inputString['val']
    tableToCreate = makeListsForNodes(inputString)
    item = createNode("create", tableToCreate)
    item.TransformToNoSQL()
    return item.toString()