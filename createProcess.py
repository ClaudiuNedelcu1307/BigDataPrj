from createNode import createNode
from createViewNode import createViewNode
import re

delTokens = ['create', ';','(', ',', ' ',')', 'if', 'not', 'exists', 'or', 'replace']
cmdMethod = ['table', 'view']

tableBool = None
def tableMethod():
    global tableBool
    tableBool = True
def viewMethod():
    global tableBool
    tableBool = False

def makeListsForNodes(inputString):
    for word in inputString:
        if word.lower() in cmdMethod:
            eval(str(word.lower()) + 'Method' + '()')
        elif word.lower() in delTokens:
            continue
        else:
            return word.replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("`", "")

def createQ(inputString):
    inputString = inputString['val']
    tableToCreate = makeListsForNodes(inputString)
    if tableBool == True:
        item = createNode("create", tableToCreate)
    elif tableBool == False:
        print("BADEA")
        asPart = inputString[inputString.index('as'):]
        item = createViewNode("view", tableToCreate, asPart)
    else:
        return "None"
    item.TransformToNoSQL()
    return item.toString()

# _text = re.sub(' +', ' ', "create table mata as select * from emp;".strip())

# _text = _text.replace(';', '')
# _text = _text.replace('(', ' ( ')
# _text = _text.replace(')', ' ) ')
# _text = _text.replace(',', ', ')
# _text.lower()
# _text = re.sub(' +', ' ', _text.strip())
# textList = _text.split()
# print("Codrin")
# print(textList)
# print('Something about BORDEA')
# print(createQ({'val': textList}))