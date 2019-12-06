from Node import Node
from whereNode import whereNode
from orderNode import orderNode
import re
class groupNode(Node):

    def __init__(self, name, cols, fromTbl, whereConditions, orderList, groupList):
        super().__init__(name)
        self.cols = [s.strip(',') for s in cols]
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions)
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.groupList = groupList
        self.cmd = ""
    

    def TransformToNoSQL(self):
        self.cmd = "db." + self.fromTbl[0] + ".group" # vor fi mai multe tabele???
        mainDicts = []
        if not("*" in self.cols):
            colsDict = {}
            for col in self.cols:
                colsDict[str(col)] = 1
            mainDicts.append(colsDict)
        elif len(self.cols) > 1:
            raise Exception('Invalid syntax: {}'.format(self.cols))

        if self.whereN:
            mainDicts.append(self.whereN.createConditionDict())

        self.cmd += str(mainDicts)

        if self.order:
            self.cmd += self.order.createOrderCommand()

        self.cmd += ';'

    
    def __str__(self):
        print(self.cmd)
        return ""
