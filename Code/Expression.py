import numpy as np

class Expression:
    def inferFunction(self, input, function):
        try:
            index = input.index(function)
        except: 
            return input
        if (index > 0):    
            input = input[:index] + "*" + input[index:]
        index = input.index(function) + len(function) + 1
        if (input[index - 1] not in "({["):
            print("ERROR: '(' expected after '" + function + "'.")
            return input
        if (input[index] in ")}]"):
            print("Error: Unexpected '" + input[index] + "' after '" + input[index - 1] + "'.")
            return input
        
        parenthesisOpen = 0
        while (index < len(input)):
            if (input[index] in "({["):
                parenthesisOpen += 1
            elif (input[index] in ")}]"):
                if (parenthesisOpen > 0):
                    parenthesisOpen -= 1
                else:
                    if (index < len(input) - 1):
                        input = input[:index + 1] + '*' + input[index + 1:]
                    return input
            index += 1
        return input     
                
    def __init__(self, input, original = False):
        self.expressions = []
        self.operations = []
        self.function = ""
        self.operators = "+-*/^"
        self.functions = ["arcsinh", "arccosh", "arctanh", "sinh", "cosh", "tanh", "arcsin", "arccos", "arctan", "cos", "sin", "tan", "exp", "ln"]
        if (original == False and input[0] in "({[" and input[len(input) - 1] in "]})"):
            input = input[1:len(input) - 1]
        for i in range (len(self.operators)):
            if (self.operators[i] in input):
                self.decompose(input, self.expressions, self.operations)
                return
        
        if (len(self.expressions) == 0):
            for function in self.functions:
                oldInput = input
                input = self.inferFunction(input, function)
                if (oldInput != input):
                    self.decompose(input, self.expressions, self.operations)
                    return
                
        for function in self.functions:
            if (function in input):
                self.function = function
                input = input.replace(function, "")
        self.expressions.append(input)
        
    def evaluate(self, variables, values):
        value = 1
        input = self.expressions[0]
        if (isinstance(input, str)):
            i = 0
            while (i < len(input)):
                if (input[i] in variables):
                    index = variables.index(input[i])
                    value *= values[index]
                    i += 1
                    continue
                number = ""
                while(i < len(input) and input[i] in "0123456789"):
                    number += input[i]
                    i += 1
                value *= int(number)
            if (self.function == "cos"):
                return np.cos(np.deg2rad(value))
            if (self.function == "sin"):
                return np.sin(np.deg2rad(value))
            if (self.function == "tan"):
                return np.tan(np.deg2rad(value))
            if (self.function == "exp"):
                return np.exp(value)
            if (self.function == "ln"):
                return np.log(value)
            if (self.function == "tan"):
                return np.tan(np.deg2rad(value))
            if (self.function == "sinh"):
                return np.sinh(np.deg2rad(value))
            if (self.function == "cosh"):
                return np.cosh(np.deg2rad(value))
            if (self.function == "tanh"):
                return np.tanh(np.deg2rad(value))
            if (self.function == "arcsinh"):
                return np.arcsinh(np.deg2rad(value))
            if (self.function == "arccosh"):
                return np.arccosh(np.deg2rad(value))
            if (self.function == "arctanh"):
                return np.arctanh(np.deg2rad(value))
            return value
        
        value = 0
        for i in range (1, len(self.expressions)):
            if (self.operations[i - 1] == "+"):
                value += self.expressions[i - 1].evaluate(variables, values)
            if (self.operations[i - 1] == "-"):
                value -= self.expressions[i - 1].evaluate(variables, values)
            if (self.operations[i - 1] == "*"):
                value += self.expressions[i - 1].evaluate(variables, values) * self.expressions[i].evaluate(variables, values)
            if (self.operations[i - 1] == "/"):
                value += self.expressions[i - 1].evaluate(variables, values) / self.expressions[i].evaluate(variables, values)
            if (self.operations[i - 1] == "^"):
                value += self.expressions[i - 1].evaluate(variables, values) ** self.expressions[i].evaluate(variables, values)
        return value
            
    def getForm(self):
        if (isinstance(self.expressions[0], str)):
            return self.function + "(" + self.expressions[0] + ")"
        form = "("
        for i in range (len(self.operations)):
            form += self.expressions[i].getForm() + " " + self.operations[i] + " "
        form += self.expressions[len(self.expressions) - 1].getForm() + ")"
        return form
        
    def printConfirmation(self):
        input = self.getForm()
        if (input[0] in "({[" and input[len(input) - 1] in "]})"):
            input = input[1:len(input) - 1]
        return "Inferred function: " + input + ". Proceed (Y)?"          
                
    def decompose(self, input, expressions, operations):
        counter, lastExpression, parenthesisOpen = 0, 0, 0
        while (counter < len(input)):
            if (input[counter] in "({["):
                parenthesisOpen += 1
            elif (parenthesisOpen == 0 and input[counter] in self.operators):
                expressions.append(Expression(input[lastExpression: counter]))
                operations.append(input[counter])    
                lastExpression = counter + 1
            elif (input[counter] in "]})"):
                if (parenthesisOpen > 0):
                    parenthesisOpen -= 1
                else:
                    print("ERROR: Unexpected '" + input[counter] + "' at position " + str(counter + 1) + ".")
                    return
            counter += 1
        expressions.append(Expression(input[lastExpression: counter]))
        
def KindInput(Type):
    """Takes the input and changes or rejects it based on the type of word/number inputted.
    Parameters
    -----------
    Type - asks the user for an input in the command line. If the user inputs a value that is not a useable type it will ask the user to try again. 
    Example
    -------
    KindInput(Float):
    
    ##output = this will ask user in command line for an input rather that in the python code."""
    Check=False
    while Check is False:
        Input=input()
        if Type==float:
            try:
                float(Input)
                Check=True
            except:
                print(f"{Input} cannot be converted to {Type}, please try again")
        if Type==int:
            try:
                int(Input)
                Check=True
            except:
                print(f"{Input} cannot be converted to {Type}, please try again")
        if Type==str:
            try:
                str(Input)
                Check=True
            except:
                print(f"{Input} cannot be converted to {Type}, please try again")
    return Input

expression = Expression(KindInput(str), True)
print(expression.printConfirmation())
print(expression.evaluate(["x", "a"], [1, 2]))