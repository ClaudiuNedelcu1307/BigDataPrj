from Node import Node
from whereNode import whereNode
from orderNode import orderNode
from colsNode import colsNode
import re
class insertNode(Node):
    
    def __init__(self, name, intoTable, cols, values):
        super().__init__(name)
        self.intoTable = intoTable
        self.cols = cols
        self.values = values
        self.cmd = ""
    

    def TransformToNoSQL(self):
        self.cmd = "db." + self.intoTable[0] + ".insert" 
        mainDict = {}

        for i in range(len(self.cols)):
            mainDict[self.cols[i]] = self.values[i]
        
        self.cmd += str(mainDict)

        self.cmd += ';'

    def toString(self):
        return self.cmd