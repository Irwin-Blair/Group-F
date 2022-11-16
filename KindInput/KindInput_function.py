# My modified KindInput function is below
def KindInput(Type):
    """Makes sure the input is an acceptable type for the program to run. It also cuts out unnecessary characters like spaces.
    
    Parameters
    ------------
    Type = the kind of input the user is inserting
    E.g. string = "Hello world" or float = 0.4643


    input1 = This is what the user inputs
    E.g. Hello world or 0.4643


    Example
    ------------
    This function would be run in the command line, as the user inputs a float, string or integer
    KindInput(input, variable_type)
    
    """
    import re
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
                Input = Input.replace(" ","")   #  Cuts out spaces
                Input = re.sub('[£$%&@?\#]', '', Input)  # Cuts out non-wanted characters
                
                # Start of check for rogue operators at start or end
                bad_chars = ["x","+","-","/","*","^"]
                if (Input[0]) in bad_chars or (Input[-1]) in bad_chars:
                    raise ValueError()
                else:
                    Check=True             
                # End of rogue operator check
                
            except:
                print(f"{Input} cannot be converted to {Type}, please try again. Make sure the function input does not begin or end with an operator")
                break
    return Input
