from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
from groupFunctionsNode import groupFunctionsNode
import re

SPECIALS = ['sum(', 'dif(', 'count(', 'max(', 'min(']

class groupNode(Node):

    def __init__(self, name, cols, fromTbl, whereConditions, orderList, groupList):
        super().__init__(name)
        # [re.search('\(([^)]+)', s.strip(',')).group(1) for s in cols]
        cols = self.taranie(cols)
        self.colsN = colsNode('cols', [s.strip(',') for s in groupList]) 
        self.initials = [s.strip(',').replace('(', '').replace(')', '').replace('*', 'star') for s in cols if any(substring in s for substring in SPECIALS) ]
        self.functions = [s.strip(',').split('(')[0] for s in cols if any(substring in s for substring in SPECIALS) ]
        self.functionsParams = [s.strip(',').split("(", 1)[1].replace(')', '').replace('*', 'star') for s in cols if any(substring in s for substring in SPECIALS)]
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.groupList = groupList
        self.cmd = ""

    def taranie(self, cols): # ASTA E MARE TARANIE .. SCHIMBA !!! FA CEVA INTELIGENT 
        # IN LISTA COLS AM : ['sum', '(', 'a', ')', ',', 'b']
        # AM NEVOIE : ['sum(a)', 'b']
        aux = ''
        SPECIALS2 = ['sum', 'count', 'min', 'max', 'count', '(']
        newCols = []
        for word in cols:
            if word == ',':
                continue
            if word == ')':
                aux += word
                newCols.append(aux)
                aux = ''
            elif word in SPECIALS2:
                aux += word
            elif len(aux) > 0:
                aux += word
            else:
                aux += word
                newCols.append(aux)
                aux = ''
        return newCols
    

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".group(" # vor fi mai multe tabele???
        mainDict = {}

        # SELECT
        selectDict = self.colsN.createColGroup()
        mainDict['key'] =  selectDict

        # INITIALS
        mainDict['initials'] = {key: 0 for key in self.initials} 

        # GROUP FUNCTIONS
        grpFncNode = groupFunctionsNode('f', zip(self.functions, self.initials, self.functionsParams))
        grpFncNode.makeFunctions()
        mainDict['reduce'] = str(grpFncNode)

        # WHERE
        if self.whereN:
            self.cmd += ', '
            whereDict = self.whereN.createConditionDict()
            mainDict['cond'] = whereDict

        # ORDER
        if self.order:
            self.cmd += self.order.createOrderCommand(self.colsN.getList())

        # FINAL
        self.cmd += str(mainDict)
        self.cmd += ');'

    
    def toString(self):
        return self.cmd

    def __str__(self):
        print(self.cmd)
        return ""

