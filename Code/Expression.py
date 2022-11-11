from Potential_Function import KindInput

class expression:
    def __init__(self, input):
        self.expressions = []
        self.operations = []
        operators = "+-*/^"
        if (input[0] in "({["):
            input = input[1:]
        if (input[len(input) - 1] in "]})"):
            input = input[:len(input) - 1]
        for i in range (len(operators)):
            if (operators[i] in input):
                self.decompose(input, self.expressions, self.operations)
                return
        self.expressions.append(input)
        
    def evaluate(self, *variables):
        value = 0
        for i in range (1, len(self.expressions)):
            if (self.operations[i - 1] == "+"):
                value += self.expressions[i - 1].evaluate(*variables)
            if (self.operations[i - 1] == "-"):
                value -= self.expressions[i - 1].evaluate(*variables)
            if (self.operations[i - 1] == "*"):
                value += self.expressions[i - 1].evaluate(*variables) * self.expressions[i].evaluate(*variables)
            if (self.operations[i - 1] == "/"):
                value += self.expressions[i - 1].evaluate(*variables) / self.expressions[i].evaluate(*variables)
            if (self.operations[i - 1] == "^"):
                value += self.expressions[i - 1].evaluate(*variables) ** self.expressions[i].evaluate(*variables)
        return value
            
    def getForm(self):
        form = "("
        if (isinstance(self.expressions[0], str)):
            return self.expressions[0]
        for i in range (len(self.operations)):
            form += self.expressions[i].getForm() + " " + self.operations[i] + " "
        form += self.expressions[len(self.expressions) - 1].getForm() + ")"
        return form
        
    def printConfirmation(self):
        print("Inferred function: " + self.getForm() + ". Proceed (Y)?")            
                
    def decompose(self, input, expressions, operations):
        counter, lastExpression, parenthesisOpen = 0, 0, 0
        while (counter < len(input)):
            if (input[counter] in "({["):
                parenthesisOpen += 1
            elif (parenthesisOpen == 0 and input[counter] in "+-*/^"):
                expressions.append(expression(input[lastExpression: counter]))
                operations.append(input[counter])    
                lastExpression = counter + 1
            elif (input[counter] in "]})"):
                if (parenthesisOpen > 0):
                    parenthesisOpen -= 1
                else:
                    print("ERROR: Unexpected '" + input[counter] + "' at " + str(counter) + ".")
                    return
            counter += 1
        expressions.append(expression(input[lastExpression: counter]))           

def getCustomFunction(input):
    function = expression(input)
    function.printConfirmation()
    input = KindInput(str)
    if (input.upper() == "Y"):
        print("Proceeding")
        #Print Graph method here, get variable values from user. Call function.evaluate(variables) to get a value for the function.
    else:
        print("Trying again")
        #Get new input here and call the function again.      