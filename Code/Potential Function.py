def User_Defined_Potential(x):
    import numpy as np
    """Fills in string Potential with corresponding potentials. Accepts a single dimensional list or array as x, outputs the potential function."""
    print("Please input the desired form of a potential function\nCurrently inbuilt funtions are:\nStep\nQuantum Harmonic Oscillator (QHO)\nSquare Well\nBarrier\nIf you want to input a custom function, please input Custom.")
    Input=input().upper()
    Potential=[]
    #Include the potential function here. This example is a step function at x=0.
    if "CUSTOM" in Input:
        print("Please enter your desired function. Please note that negatives must be written as +-")
        Custom_Input=input().upper()
        Custom_Function=Custom_Input.split("+")
        Potential=np.zeros(len(x))
        for j in range(len(x)):
            for i in range(len(Custom_Function)):
                if "X" in Custom_Function[i]:
                    Coefficient,Exponent=Custom_Function[i].split("X")
                    #Dealing with the possible lack of coeffients if the value has a coefficient of either +1 or -1
                    if Coefficient=="":
                        Coefficient=str(1)
                    if Coefficient=="-":
                        Coefficient=str(-1)
                    #Dealing with the possibility of user not inputting an exponent of 1
                    if Exponent=="":
                        Exponent=str(1)
                    #Dealing with people putting exponential symbols in
                    if "**" in Exponent:
                        Exponent=Exponent.replace("**","")
                    if "^" in Exponent:
                        Exponent=Exponent.replace("^","")
                    #Converting them back to floats, as we can't do mathematical operations on strings
                    Coefficient,Exponent=float(Coefficient),float(Exponent)
                    Potential[j]+=Coefficient*x[j]**Exponent
                else:
                    #Checking that in case the user gave a constant, therefore no X, we can add that.
                    Potential[j]+=float(Custom_Function[i])
    elif "STEP" in Input:
        print("Do you want to customize the step function? Default is 0 in case x<0, 1 if x>0")
        Input=input().upper()
        if "Y" in Input:
            print("Please enter the desired amplitude")
            Amplitude=float(input())
            print("Please enter where you want the step to happen")
            Wherestep=float(input())
            print("Do the values of x have to be greater than or less than this value to get the amplitude?")
            GreaterThanLessThan=input().upper()
            if "<" in GreaterThanLessThan or "G" in GreaterThanLessThan:
                for i in x:
                    if i>Wherestep:
                        Potential.append(Amplitude)
                    else:
                        Potential.append(0)
            else:
                for i in x:
                    if i<Wherestep:
                        Potential.append(Amplitude)
                    else:
                        Potential.append(0)
        else: #This can lead to odd effects, like chicken giving a default step function, but anyone doing that isn't serious.
            for i in x:
                if i>0:
                    Potential.append(1)
                else:
                    Potential.append(0)
    elif "QUANTUM HARMONIC OSCILLATOR" in Input or "HARMONIC OSCILLATOR" in Input or "OSCILLATOR" in Input or "QHO" in Input:
        for i in x:
            Potential.append(i**2)
    elif "WELL" in Input:
        #Adding values here as magic numbers in case we want to allow the user to change them.
        Distance_to_wall=0.5
        Amplitude=1
        for i in x:
            if np.abs(i)>Distance_to_wall:
                Potential.append(Amplitude)
            else:
                Potential.append(0)
    elif "BARRIER" in Input:
        #Adding values here as magic numbers in case we want to allow the user to change them.
        Distance_to_wall=0.5
        Barrier_Width=0.1
        Barrier_Location=0
        Barrier_Amplitude=0.7
        Amplitude=1
        for i in x:
            if np.abs(i)>Distance_to_wall:
                Potential.append(Amplitude)
            else:
                if i<Barrier_Location+(Barrier_Width*0.5) and i>Barrier_Location-(Barrier_Width*0.5):#Keeping the barrier width same
                    Potential.append(Barrier_Amplitude)
                else:
                    Potential.append(0)
    return Potential


#Testing that potential comes out as desired
import matplotlib.pyplot as plt
import numpy as np
x=np.linspace(-1,1)
plt.plot(x,User_Defined_Potential(x))
#TODO: add user definition of variables for Well,Barrier, and Quantum Harmonic Oscillator.
