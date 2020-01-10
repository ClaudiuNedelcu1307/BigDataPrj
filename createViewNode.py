from Node import Node
import re
class createViewNode(Node):
    
    def __init__(self, name, table, asPart):
        super().__init__(name)
        self.table = table
        self.asPart = asPart
        print(asPart)
        self.cmd = ""
    

    def TransformToNoSQL(self):
        # CREATE
        self.cmd = "db.createView(\"" + self.table + "\");"

    def toString(self):
        return self.cmd

