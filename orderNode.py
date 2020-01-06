from Node import Node

class orderNode(Node):

    def __init__(self, name, orderList):
        super().__init__(name)
        self.orderList = orderList

    def createOrderCommand(self, cols):
        if len(self.orderList) == 0:
            return ""

        retDict = {}
        for word in self.orderList:
            if word == 'asc':
                retDict[list(retDict.keys())[-1]] = 1
            elif word == 'desc':
                retDict[list(retDict.keys())[-1]] = -1
            elif word.isdigit():
                retDict[cols[int(word) - 1]] = 1
            else:
                retDict[word] = 1

        return ".sort(" + str(retDict) + ")"