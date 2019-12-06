from Node import Node

class groupFunctionsNode(Node):

    def __init__(self, name, functions):
        super().__init__(name)
        self.arithmetics = ['sum', 'dif']
        self.functions = functions
        self.cmd = ''

    def arithmeticFunc(self, function):
        if function in self.arithmetics:
            return True
        return False

    def makeFunctions(self):
        self.cmd += 'function(prev, obj) {\n'

        for (function, initial, obj) in self.functions:
            print(function, initial, obj)
            line = 'prev.'
            if self.arithmeticFunc(function):
                line += initial + ' = prev.' + initial + ' + obj.' + obj + ' - 0;' + '\n'

            self.cmd += line
        self.cmd += '}'

    def __str__(self):
        return self.cmd