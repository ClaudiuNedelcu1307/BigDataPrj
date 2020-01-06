from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class findNode(Node):
    
    def __init__(self, name, cols, fromTbl, whereConditions, orderList, limit):
        super().__init__(name)
        self.colsN = colsNode('cols', [s.strip(',') for s in cols])
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.limit = limit[0] if len(limit) > 0 else 0
        self.cmd = ""

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".find("

        # SELECT
        selectDict = self.colsN.createCols()
        self.cmd += str(selectDict)

        # WHERE
        if self.whereN:
            self.cmd += ', '
            whereDict = self.whereN.createConditionDict()
            self.cmd += str(whereDict)
        
        # FINAL
        self.cmd += ')'

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
