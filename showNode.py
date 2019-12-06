from Node import Node
import re

class showNode(Node):

    def __init__(self, name, whatToShow):
        super().__init__(name)
        self.whatToShow = whatToShow
        self.cmd = ""
    
    def TransformToNoSQL(self):
        self.cmd = "show " + self.whatToShow

    def toString(self):
        return self.cmd

    def __str__(self):
        print(self.cmd)
        return ""
