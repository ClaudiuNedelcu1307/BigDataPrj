from Node import Node
import re
class dropNode(Node):
    
    def __init__(self, name, table):
        super().__init__(name)
        self.table = table
        self.cmd = ""
    

    def TransformToNoSQL(self):
        # DROP
        self.cmd = "db." + self.table + ".drop();"

    def toString(self):
        return self.cmd

