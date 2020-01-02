from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class joinNode(Node):
    
    def __init__(self, name, cols, fromTbl, whereConditions, orderList, join, on, using):
        super().__init__(name)
        self.colsN = colsNode('cols', [s.strip(',') for s in cols])
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        print(on, 'sfsdf', on[0])
        self.joinCond = on[0] if len(on) > 0 else using[0]
        self.joinTable = join
        self.cmd = ""

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db.getCollection(" + self.fromTbl[0] + ").aggregate("
        dictList = []

        # SELECT
        # selectDict = self.colsN.createCols()
        # self.cmd += str(selectDict)

        # PROJECT
        auxDict = {'_id': 'NumberInt(0)', self.fromTbl[0]: "$$ROOT"}
        projectDict = {'$lookup': auxDict}
        dictList.append(projectDict)

        # ON / USING
        auxDict = {'localField': self.joinCond, "from":self.fromTbl[0], 'foreignField':self.joinCond.split('.')[1], 'as':self.fromTbl[0]}
        onDict = {'$lookup':auxDict}
        dictList.append(onDict)
        
        # WHERE
        if self.whereN:
            print("Cavendish")
            whereDict = {'$match':{}}
            # self.cmd += str(whereDict)
            whereDict['$match'] = self.whereN.createConditionDict()
            dictList.append(whereDict)

        #UNWIND
        auxDict = {'path': '$' + self.joinTable[0], "preserveNullAndEmptyArrays": False}
        unwindDict = {'$unwind': auxDict}
        dictList.append(unwindDict)

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
