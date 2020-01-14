from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
from groupFunctionsNode import groupFunctionsNode
import re

SPECIALS = ['sum(', 'dif(', 'count(', 'max(', 'min(', 'avg(']

class groupNode(Node):

    def __init__(self, name, cols, fromTbl, whereConditions, orderList, groupList, limit):
        super().__init__(name)
        cols = self.taranie(cols)
        self.colsN = colsNode('cols', [s.strip(',') for s in groupList]) 
        self.initials = [s.strip(',').replace('(', '').replace(')', '').replace('*', 'star') for s in cols if any(substring in s for substring in SPECIALS) ]
        self.functions = [s.strip(',').split('(')[0] for s in cols if any(substring in s for substring in SPECIALS) ]
        self.functionsParams = [s.strip(',').split("(", 1)[1].replace(')', '').replace('*', 'star') for s in cols if any(substring in s for substring in SPECIALS)]
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.groupList = groupList
        self.limit = limit[0] if len(limit) > 0 else 0
        self.cmd = ""  

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".group("
        mainDict = {}

        # SELECT
        selectDict = self.colsN.createColGroup()
        mainDict['key'] =  selectDict

        # GROUP FUNCTIONS
        grpFncNode = groupFunctionsNode('f', zip(self.functions, self.initials, self.functionsParams))
        (weNeedFinalize, finalizeList) = grpFncNode.makeFunctions()

        # FINALIZE
        if weNeedFinalize == True:
            strFinalize = self.makeFinalize(finalizeList)
            for item in finalizeList:
                self.initials.append('count' + item)

        # INITIALS & more
        mainDict['initials'] = {key: 0 for key in self.initials} 
        mainDict['reduce'] = str(grpFncNode)
        if weNeedFinalize:
            mainDict['finalize'] = strFinalize

        # WHERE
        if self.whereN:
            whereDict = self.whereN.createConditionDict()
            mainDict['cond'] = whereDict
        
        # FINAL
        self.cmd += str(mainDict)
        self.cmd += ')\n'

        # LIMIT
        if not(self.limit == 0):
            self.cmd += ".limit(" + self.limit + ")"

        # ORDER
        if self.order:
            self.cmd += self.order.createOrderCommand(self.colsN.getList())
        
        self.cmd += ';'

    def toString(self):
        return self.cmd

    def __str__(self):
        print(self.cmd)
        return ""

    def makeFinalize(self, finalizeList):
        cmd = 'function(prev) {\n'

        for item in finalizeList:
            line = ''
            line += 'prev.average' + item + ' = prev.' + item + ' / prev.' + 'count' + item + '\n'
            line += 'delete ' + 'count' + item + ' \n'
            line += 'delete ' + item + ' \n'
            cmd += line
        cmd += '}'
        return cmd
