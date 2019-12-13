from Node import Node

class whereNode(Node):

    tokens = ['and', 'or']
    InvOperands = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '=': '!=', '!=': '=', 'is':'!='}

    signDict = {'>': '$gt', '<': '$lt', '>=': '$gte', '<=': '$lte', '!=': '$ne'}
    SIGNS = ['>', '<', '>=', '<=', '!=']

    FUNCTIONS = ['upper', 'lower']

    def __init__(self, name, whereConditions):
        super().__init__(name)
        self.whereConditions = whereConditions
        self.st = []
        self.infix = []

    def RepresentsNumber(self, s):
        try: 
            float(s)
            return True
        except ValueError:
            return False

    def upperFunc(self, input):
        return input['val'].upper()
    def lowerFunc(self, input):
        return input['val'].lower()

    def packCondition(self, condition):
        # adaug upper si lower

        for function in self.FUNCTIONS:
            if function in condition:
                tempDict = {}
                tempDict['val'] = condition[condition.index(function) + 1]
                condition[condition.index(function) + 1] = eval('self.' + function + 'Func' + '(' + str(tempDict) + ')')
                condition.remove(function)
        if condition[0] == 'not' and condition[2] == 'in':
            return (condition[1], {'$not': {"$in": [word.translate({ord(i): None for i in '(),'}) for word in condition[3:]]}})

        if condition[0] == 'not':
            condition.pop(0)
            condition[1] = self.InvOperands[condition[1]]

        if condition[1] == 'not' and condition[2] == 'in':
            return (condition[0], {'$not': {"$in": [word.translate({ord(i): None for i in '(),'}) for word in condition[3:]]}})
        elif condition[1] == 'like':
            return (condition[0], condition[2].replace("'", ""))
        elif condition[1] == 'in':
            return (condition[0], {"$in": [word.translate({ord(i): None for i in '(),'}) for word in condition[2:]]})
        elif condition[1] == 'is' and condition[2] == 'not':
            return (condition[0], {"$ne": condition[3].replace("'", "")})
        elif condition[1] == 'is':
            return (condition[0], condition[2].replace("'", ""))
        # elif self.RepresentsNumber(condition[0]) == False  and self.RepresentsNumber(condition[2]) == False:
        #     return ("$where", "this." + str(condition[0]) + " " + str(condition[1]) + " this." + str(condition[2]))
        elif condition[1] in self.SIGNS:
            return (condition[0].replace("'", ""), {self.signDict[condition[1]]: condition[2].replace("'", "") if not(self.RepresentsNumber(condition[2].replace("'", ""))) else float(condition[2].replace("'", ""))})
        elif condition[1] == '=':
            return (condition[0].replace("'", ""), condition[2].replace("'", "") if not(self.RepresentsNumber(condition[2].replace("'", ""))) else float(condition[2].replace("'", "")))
        
        return (condition[0], None)

    def prec(self, c): 
        if c == 'and': 
            return 3 
        if c == 'or': 
            return 2
        return 1

    # Return the value of the top of the stack 
    def peek(self): 
        return self.st[-1] 
      
    # Pop the element from the stack 
    def pop(self): 
        if len(self.st) > 0: 
            return self.st.pop() 
        else: 
            return "$"
      
    # Push the element to the stack 
    def push(self, op): 
        self.st.append(op)

    def infixToPostfix(self): 
        self.push('N')
        ns = []
        oneCond = []
        isInStatement = False
        for word in self.whereConditions:

            if isInStatement or (word not in self.tokens and word not in ['(', ')']): 
                oneCond.append(word) 
            elif word == '(':
                print("SUPER DUPER MAN")
                self.push(word)
            elif word == ')':
                if len(oneCond) > 0:
                    ns.append(self.packCondition(oneCond))
                    oneCond = []
                while not(self.peek() == 'N') and self.peek() != '(':
                    c1 = self.peek()
                    self.pop()
                    ns.append(c1)
  
                if self.peek() == '(':
                    self.pop()
            elif word in self.tokens: 
                if len(oneCond) > 0:
                    ns.append(self.packCondition(oneCond))
                    oneCond = []
                while not(self.peek() == 'N') and self.prec(word) <= self.prec(self.peek()): 
                    c2 = self.peek()
                    self.pop()
                    ns.append(c2)

                self.push(word)  
        
        if len(oneCond) > 0:
            ns.append(self.packCondition(oneCond))
            oneCond = []
        # Pop all the remaining elements from the stack
        while not(self.peek() == 'N'):
            c3 = self.peek()
            self.pop()
            ns.append(c3)
        return ns

    def getInfix(self, exp):
        st = []
        for word in exp:
            # Push operands
            if word not in self.tokens:
                (key, value) = word
                st.append({key: value})
            # Operator
            else:
                tempList = []
                tempList.append(st.pop())
                tempList.append(st.pop())

                st.append({word: tempList})
        return st.pop()
  
    
    def createConditionDict(self):
        return self.getInfix(self.infixToPostfix())
        