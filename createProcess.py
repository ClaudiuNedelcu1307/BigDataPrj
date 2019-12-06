from createNode import createNode

def createQ(inputString):
    inputString = inputString['val']
    item = createNode("create", inputString[2])
    item.TransformToNoSQL()
    return item.toString()