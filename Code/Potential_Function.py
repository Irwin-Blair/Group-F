# def User_Defined_Potential(x):
#     import numpy as np
#     """Fills in string Potential with corresponding potentials. Accepts a single dimensional list or array as x, outputs the potential function."""
#     print("Please input the desired form of a potential function\nCurrently inbuilt funtions are:\nStep\nQuantum Harmonic Oscillator (QHO)\nSquare Well\nBarrier\nIf you want to input a custom function, please input Custom.")
#     Function_Choice=KindInput(str)
#     Function_Choice_Capitalized=Function_Choice.upper()
#     Potential=[]
#     #Include the potential function here. This example is a step function at x=0.
#     if "CUSTOM" in Function_Choice_Capitalized:
#         print("Please enter your desired function. Please note that negatives must be written as +-")
#         Custom_Input=KindInput(str).upper()
#         Custom_Function=Custom_Input.split("+")
#         Potential=np.zeros(len(x))
#         for j in range(len(x)):
#             for i in range(len(Custom_Function)):
#                 if "X" in Custom_Function[i]:
#                     Coefficient,Exponent=Custom_Function[i].split("X")
#                     #Dealing with the possible lack of coeffients if the value has a coefficient of either +1 or -1
#                     if Coefficient=="":
#                         Coefficient=str(1)
#                     if Coefficient=="-":
#                         Coefficient=str(-1)
#                     #Dealing with the possibility of user not inputting an exponent of 1
#                     if Exponent=="":
#                         Exponent=str(1)
#                     #Dealing with people putting exponential symbols in
#                     if "**" in Exponent:
#                         Exponent=Exponent.replace("**","")
#                     if "^" in Exponent:
#                         Exponent=Exponent.replace("^","")
#                     #Converting them back to floats, as we can't do mathematical operations on strings
#                     Coefficient,Exponent=float(Coefficient),float(Exponent)
#                     Potential[j]+=Coefficient*x[j]**Exponent
#                 else:
#                     #Checking that in case the user gave a constant, therefore no X, we can add that.
#                     Potential[j]+=float(Custom_Function[i])
#     #Defining some pre-determined functions. If adding more, dont forget to add them to the print statement on line 9. (07/11/2022)
#     elif "STEP" in Function_Choice_Capitalized:
        
#         #Defining default values to reduce if/else bloat
#         Upper_Amplitude=1
#         Lower_Amplitude=0
#         Wherestep=0
#         GreaterThanLessThan="L"
        
#         print("Do you want to customize the step function? Default is 0 in case x<0, 1 if x>0")
#         Input=KindInput(str).upper()
#         if "Y" in Input:
#             print("Please enter the desired upper amplitude")
#             Upper_Amplitude=float(KindInput(float))
#             print("Please enter the desired lower amplitude")
#             Lower_Amplitude=float(KindInput(float))
#             print("Please enter where you want the step to happen")
#             Wherestep=float(KindInput(float))
#             print("Do the values of x have to be greater than or less than this value to get the upper amplitude?")
#             GreaterThanLessThan=input().upper()
#         if "<" in GreaterThanLessThan or "G" in GreaterThanLessThan:
#             for i in x:
#                 if i>Wherestep:
#                     Potential.append(Upper_Amplitude)
#                 else:
#                     Potential.append(Lower_Amplitude)
#         else:
#             for i in x:
#                 if i<Wherestep:
#                     Potential.append(Upper_Amplitude)
#                 else:
#                     Potential.append(Lower_Amplitude)
#     elif "OSCILLATOR" in Function_Choice_Capitalized or "QHO" in Function_Choice_Capitalized:
        
#         #Defining default values to reduce if/else bloat
#         k=1
        
#         print("Do you want to customize the Quantum Harmonic Oscillator? Default is k*x**2, where k=1")
#         Input=KindInput(str).upper()
#         if "Y" in Input:
#             print("Please choose an alternate value of k (If a more complex form is desired, use the custom command)")
#             k=float(KindInput(float))
#         for i in x:
#             Potential.append(k*i**2)
#     elif "WELL" in Function_Choice_Capitalized:
        
#         #Defining default values to reduce if/else bloat
#         Distance_to_wall=1
#         Upper_Amplitude=1
#         Lower_Amplitude=0
#         Well_Center=0
        
#         print("Do you want to customize the well? Default is 0 if -1<x<1, 1 otherwise")
#         Input=KindInput(str).upper()
#         if "Y" in Input:
#             print("Where do you want to center the well?")
#             Well_Center=float(KindInput(float))
#             print("What amplitude do you want the walls of the well to have?")
#             Upper_Amplitude=float(KindInput(float))
#             print("What amplitude is the center of the well?")
#             Lower_Amplitude=float(KindInput(float))
#             print("What width do you want the well to have?")
#             Distance_to_wall=float(KindInput(float))/2
#         for i in x:
#             if i>Well_Center+Distance_to_wall or i<Well_Center-Distance_to_wall:
#                 Potential.append(Upper_Amplitude)
#             else:
#                 Potential.append(Lower_Amplitude)
#     elif "BARRIER" in Function_Choice_Capitalized:
        
#         #Defining default values to reduce if/else bloat
#         Number_of_barriers=1
#         Distance_to_wall=2.5
#         Barrier_Width=[0.1]
#         Barrier_Location=[0]
#         Barrier_Amplitude=[0.5]
#         Upper_Amplitude=1
#         Lower_Amplitude=0
#         Well_Center=0
        
#         print("Do you want to customize the barriers? Default is a single barrier of amplitude 0.5 at location x=0, with a with of 0.1, in a well of width 5 centered on x=0")
#         Input=KindInput(str).upper()
#         if "Y" in Input:
#             Barrier_Amplitude=[]
#             Barrier_Location=[]
#             Barrier_Width=[]
#             print("Where do you want to center the well?")
#             Well_Center=float(KindInput(float))
#             print("What amplitude do you want the walls of the well to have?")
#             Upper_Amplitude=float(KindInput(float))
#             print("What amplitude is the center of the well?")
#             Lower_Amplitude=float(KindInput(float))
#             print("What width do you want the well to have?")
#             Distance_to_wall=float(KindInput(float))/2
#             print("How many barriers do you want?")
#             Number_of_barriers=int(KindInput(int))
#             #Getting the barrier locations
#             for i in range(Number_of_barriers):
#                 if str(i+1)[-1]=="0":
#                     Number_Ending="th"
#                 elif str(i+1)[-1]=="1":
#                     Number_Ending="st"
#                 elif str(i+1)[-1]=="2":
#                     Number_Ending="nd"
#                 else:
#                     Number_Ending="rd"
#                 print(f"The following is for the {i+1}{Number_Ending} barrier")
#                 print("Where is the barrier located?")
#                 Barrier_Location.append(float(KindInput(float)))
#                 print("What is the amplitude of this barrier?")
#                 Barrier_Amplitude.append(float(KindInput(float)))
#                 print("How wide is this barrier?")
#                 Barrier_Width.append(float(KindInput(float)))
#         #Defining the well that the barriers sit in.
#         for i in x:
#             if i>Well_Center+Distance_to_wall or i<Well_Center-Distance_to_wall:
#                 Potential.append(Upper_Amplitude)
#             else:
#                 Potential.append(Lower_Amplitude)
#         #Adding the barriers
#         for i in range(len(x)):
#             for j in range(len(Barrier_Location)):
#                 BCenter=Barrier_Location[j]
#                 BWidth=Barrier_Width[j]/2
#                 BAmplitude=Barrier_Amplitude[j]
#                 X=x[i]
#                 if BCenter-BWidth<X<BCenter+BWidth:
#                     if Potential[i]<BAmplitude:
#                         Potential[i]=BAmplitude
#     return np.array(Potential),Function_Choice


# My changes are below
stringin = "hello+"
def KindInput(Type):
    """Takes an input that doesn't crash program if it can't be used."""
    Check=False
    while Check is False:
        Input=stringin
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




#Testing that potential comes out as desired
#import matplotlib.pyplot as plt
#import numpy as np
#x=np.linspace(-5,5,num=1000)
#plt.plot(x,User_Defined_Potential(x)[0])
#TODO: add user definition of variables for Well,Barrier, and Quantum Harmonic Oscillator.
