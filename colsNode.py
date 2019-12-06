from Node import Node

class colsNode(Node):

    def __init__(self, name, colsList):
        super().__init__(name)
        self.colsList = colsList

    def createCols(self):
        if not("*" in self.colsList):
            colsDict = {}
            for col in self.colsList:
                colsDict[str(col)] = 1
            return colsDict
        return {}