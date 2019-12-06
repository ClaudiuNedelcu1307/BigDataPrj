from Node import Node
import re
class createNode(Node):
    
    def __init__(self, name, table):
        super().__init__(name)
        self.table = table
        self.cmd = ""
    

    def TransformToNoSQL(self):
        # CREATE
        self.cmd = "db.createCollection(\"" + self.table + "\");"

    def toString(self):
        return self.cmd

