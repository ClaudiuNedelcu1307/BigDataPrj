from Node import Node

class groupFunctionsNode(Node):

    def __init__(self, name, functions):
        super().__init__(name)
        self.arithmetics = ['sum', 'dif']
        self.counts = ['countstar']
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
            line = ''
            if self.arithmeticFunc(function):
                line += 'prev.' + initial + ' = prev.' + initial + ' + obj.' + obj + ' - 0;' + '\n'
            elif function in self.counts:
                line += 'if (true != null) if (true instanceof Array) prev.' + initial +' += true.length;\nelse prev.' + initial + '++;\n'

            self.cmd += line
        self.cmd += '}'

    def __str__(self):
        return self.cmd