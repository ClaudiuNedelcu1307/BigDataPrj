from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
from groupFunctionsNode import groupFunctionsNode
import re
class groupNode(Node):

    def __init__(self, name, cols, fromTbl, whereConditions, orderList, groupList):
        super().__init__(name)
        self.colsN = colsNode('cols', [re.search('\(([^)]+)', s.strip(',')).group(1) for s in cols])
        self.initials = [s.strip(',').replace('(', '').replace(')', '') for s in cols]
        self.functions = [s.strip(',').split('(')[0] for s in cols]
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions)
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.groupList = groupList
        self.cmd = ""
    

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".group(" # vor fi mai multe tabele???
        mainDict = {}

        # SELECT
        selectDict = self.colsN.createCols()
        mainDict['key'] =  selectDict

        # INITIALS
        mainDict['initials'] = {key: 0 for key in self.initials} 

        # GROUP FUNCTIONS
        grpFncNode = groupFunctionsNode('f', zip(self.functions, self.initials, self.colsN.getList()))
        grpFncNode.makeFunctions()
        mainDict['reduce'] = str(grpFncNode).replace("'", "")

        # WHERE
        if self.whereN:
            self.cmd += ', '
            whereDict = self.whereN.createConditionDict()
            mainDict['cond'] = whereDict
            # self.cmd += str(whereDict)

        # ORDER
        if self.order:
            self.cmd += self.order.createOrderCommand()

        # FINAL
        self.cmd += ');'
        print('')
        print(mainDict)
        print('Bordea')
    
    def toString(self):
        return self.cmd

    def __str__(self):
        print(self.cmd)
        return ""

