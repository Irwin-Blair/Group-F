# My modified KindInput function is below
def KindInput(Type,input1):
    """Takes an input that doesn't crash program if it can't be used."""
    import re
    Check=False
    while Check is False:
        Input=input1
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
                Input = re.sub('[£$%@?\#]', '', Input)  # Cuts out non-wanted characters
                
                # Start of check for rogue operators at start or end
                bad_chars = ["x","+","-","/"]
                if (Input[0]) in bad_chars or (Input[-1]) in bad_chars:
                    raise ValueError()
                else:
                    Check=True             
                # End of rogue operator check
                
            except:
                print(f"{Input} cannot be converted to {Type}, please try again. Make sure the function input does not begin or end with an operator")
                break
    return Input
