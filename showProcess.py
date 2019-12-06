from showNode import showNode

def showQ(inputString):
    inputString = inputString['val']
    item = showNode("show", inputString[2])
    item.TransformToNoSQL()
    return item.toString()

