from dropNode import dropNode

delTokens = ['drop', ';','(', ',', ' ',')', 'table', 'if', 'not', 'exists']

def makeListsForNodes(inputString):
    for word in inputString:
        if word.lower() in delTokens:
            continue
        else:
            return word.replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("`", "")

def dropQ(inputString):
    inputString = inputString['val']
    tableToDrop = makeListsForNodes(inputString)
    item = dropNode("drop", tableToDrop)
    item.TransformToNoSQL()
    return item.toString()

