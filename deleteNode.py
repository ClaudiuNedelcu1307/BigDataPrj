from Node import Node
import re
from whereNode import whereNode

class deleteNode(Node):
    
    def __init__(self, name, fromTbl, whereConditions):
        super().__init__(name)
        self.fromTbl = fromTbl
        self.whereN = whereNode("where", whereConditions) if len(whereConditions) > 0 else None
        self.cmd = ""
    

    def TransformToNoSQL(self):
        #FROM
        self.cmd = "db." + self.fromTbl[0] + ".delete("
        
        # WHERE
        if self.whereN:
            whereDict = self.whereN.createConditionDict()
            self.cmd += str(whereDict)

        # FINAL
        self.cmd += ');'

    def toString(self):
        return self.cmd



