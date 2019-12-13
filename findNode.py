from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class findNode(Node):
    
    def __init__(self, name, cols, fromTbl, whereConditions, orderList):
        super().__init__(name)
        self.colsN = colsNode('cols', [s.strip(',') for s in cols])
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.cmd = ""

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".find(" # vor fi mai multe tabele???

        # SELECT
        selectDict = self.colsN.createCols()
        self.cmd += str(selectDict)

        # WHERE
        if self.whereN:
            self.cmd += ', '
            whereDict = self.whereN.createConditionDict()
            self.cmd += str(whereDict)

        # ORDER
        if self.order:
            self.cmd += self.order.createOrderCommand(self.colsN.getList())

        # FINAL
        self.cmd += ');'

    def toString(self):
        return self.cmd

    
    def __str__(self):
        print(self.cmd)
        return ""
