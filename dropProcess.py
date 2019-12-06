from dropNode import dropNode

def dropQ(inputString):
    inputString = inputString['val']
    item = dropNode("drop", inputString[2])
    item.TransformToNoSQL()
    return item.toString()

