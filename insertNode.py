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
        j = 1
        for listOfValue in self.values:
            print("AICI", j, listOfValue)
            self.cmd += "db." + self.intoTable[0] + ".insert(" 
            mainDict = {}
            
            for i in range(len(self.cols)):
                mainDict[self.cols[i]] = listOfValue[i]
            
            self.cmd += str(mainDict)

            self.cmd += ');\n'
            j = j + 1
    def toString(self):
        return self.cmd