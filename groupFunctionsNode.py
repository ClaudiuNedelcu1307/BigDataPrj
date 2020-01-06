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
        weNeedFinalize = False
        finalizeList = []

        for (function, initial, obj) in self.functions:
            line = ''
            if self.arithmeticFunc(function):
                line += 'prev.' + initial + ' = prev.' + initial + ' + obj.' + obj + ' - 0;' + '\n'
            elif function == 'count' and initial == 'countstar':
                line += 'if (true != null) \
                    if (true instanceof Array) \
                        prev.' + initial +' += true.length;\n\
                    else prev.' + initial + '++;\n'
            elif function == 'count':
                line += 'if (obj.'+ obj + ' != null) \
                    if (obj.'+ obj + ' instanceof Array) \
                        prev.' + initial +' += obj.' + obj + '.length;\n\
                    else prev.' + initial + '++;\n'
            elif function == 'max':
                line += 'prev.'+ initial + ' = isNaN(prev. '+ initial + ' ? obj.' + obj + ' : Math.max(prev.' + initial + ', obj.' + obj + ');\n'
            elif function == 'min':
                line += 'prev.'+ initial + ' = isNaN(prev. '+ initial + ' ? obj.' + obj + ' : Math.min(prev.' + initial + ', obj.' + obj + ');\n'
            elif function == 'avg':
                weNeedFinalize = True
                finalizeList.append(initial)
                line += 'prev.' + initial + ' = prev.' + initial + ' + obj.' + obj + ' - 0;' + '\n'
                line += 'prev.count' + initial + '++'

            self.cmd += line
        self.cmd += '}'
        return (weNeedFinalize, finalizeList)

    def __str__(self):
        return self.cmd