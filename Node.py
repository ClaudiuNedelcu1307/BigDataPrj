class Node:

    def __init__(self, name):
        self.name = name
        self.subordinates = []
    
    def TransformToNoSQL(self):
        print("Nu.i bine Jonule")

    def taranie(self, cols): # ASTA E MARE TARANIE .. SCHIMBA !!! FA CEVA INTELIGENT 
        # IN LISTA COLS AM : ['sum', '(', 'a', ')', ',', 'b']
        # AM NEVOIE : ['sum(a)', 'b']
        aux = ''
        SPECIALS2 = ['sum', 'count', 'min', 'max', 'count', 'avg', '(']
        newCols = []
        for word in cols:
            if word == ',':
                continue
            if word == ')':
                aux += word
                newCols.append(aux)
                aux = ''
            elif word in SPECIALS2:
                aux += word
            elif len(aux) > 0:
                aux += word
            else:
                aux += word
                newCols.append(aux)
                aux = ''
        return newCols