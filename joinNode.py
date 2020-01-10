from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class joinNode(Node):
    
    def __init__(self, name, cols, fromTbl, whereConditions, orderList, join, on, using, alias, limit):
        super().__init__(name)
        self.colsN = colsNode('cols', [s.strip(',') for s in cols])
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.order = orderNode("order", [s.strip(',') for s in orderList])
        self.joinCond = on if len(on) > 0 else using
        self.joinTable = join
        self.alias = alias if len(alias) > 0 else join
        self.limit = limit[0] if len(limit) > 0 else 0
        self.cmd = ""
    
    def makeLookups(self):
        nextJoinTable = 1
        lookupDicts = []
        unwindDicts = []
        for item in range(3, len(self.joinCond), 3):
            auxDict = {'localField': self.joinCond[item], "from":self.joinTable[nextJoinTable], 'foreignField':self.joinCond[item + 2].split('.')[1], 'as':self.joinTable[nextJoinTable]}
            lookupDicts.append(auxDict)
            auxDict2 = {'path': '$' + self.joinTable[nextJoinTable], "preserveNullAndEmptyArrays": False}
            unwindDicts.append(auxDict2)
            nextJoinTable = nextJoinTable + 1 
    
        return (lookupDicts, unwindDicts)

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db.getCollection(" + self.fromTbl[0] + ").aggregate("
        dictList = []

        # PROJECT
        auxDict = {'_id': 'NumberInt(0)', self.fromTbl[0]: "$$ROOT"}
        projectDict = {'$project': auxDict}
        dictList.append(projectDict)

        # ON / USING
        auxDict = {'localField': self.joinCond[0], "from":self.joinTable[0], 'foreignField':self.joinCond[2].split('.')[1], 'as':self.joinTable[0]}
        onDict = {'$lookup':auxDict}
        dictList.append(onDict)

        # UNWIND
        auxDict = {'path': '$' + self.joinTable[0], "preserveNullAndEmptyArrays": False}
        unwindDict = {'$unwind': auxDict}
        dictList.append(unwindDict)

        (looks, unwinds) = self.makeLookups()
        for i in range(0, len(looks)):
            onDict = {'$lookup':looks}
            dictList.append(onDict)
            unwindDict = {'$unwind': unwinds}
            dictList.append(unwindDict)

        # WHERE
        if self.whereN:
            whereDict = {'$match':{}}
            whereDict['$match'] = self.whereN.createConditionDict()
            dictList.append(whereDict)

        # FINAL
        self.cmd += str(dictList)
        self.cmd += ')'

        # ORDER
        if self.order:
            self.cmd += self.order.createOrderCommand(self.colsN.getList())
        
        self.cmd += ';'

    def toString(self):
        return self.cmd

    
    def __str__(self):
        print(self.cmd)
        return ""
