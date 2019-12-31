from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class joinNode(Node):
    
    def __init__(self, name, cols, fromTbl, whereConditions, orderList, join, on):
        super().__init__(name)
        self.colsN = colsNode('cols', [s.strip(',') for s in cols])
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.cmd = ""

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db.getCollection(" + self.fromTbl[0] + ").aggregate("
        dictList = []

        # SELECT
        # selectDict = self.colsN.createCols()
        # self.cmd += str(selectDict)

        # WHERE
        if self.whereN:
            print("Cavendish")
            whereDict = {'$match':{}}
            # self.cmd += str(whereDict)
            whereDict['$match'] = self.whereN.createConditionDict()
            dictList.append(whereDict)

        # ORDER
        # if self.order:
        #     self.cmd += self.order.createOrderCommand(self.colsN.getList())

        # FINAL
        self.cmd += str(dictList)
        self.cmd += ');'

    def toString(self):
        return self.cmd

    
    def __str__(self):
        print(self.cmd)
        return ""
