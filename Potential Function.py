# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:46:38 2022

@author: iarla
"""

def User_Defined_Potential(x):
    import numpy as np
    """Fills in string Potential with corresponding potentials"""
    print("Please input the desired form of a potential function\nCurrently inbuilt funtions are:\nStep\nQuantum Harmonic Oscillator (QHO)\nIf you want to input a custom function, please input Custom.")
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
                    #Dealing with the folly of man
                    if Coefficient=="":
                        Coefficient=str(1)
                    if Coefficient=="-":
                        Coefficient=str(-1)
                    if Exponent=="":
                        Exponent=str(1)
                    if "**" in Exponent:
                        Exponent=Exponent.replace("**","")
                    Coefficient,Exponent=float(Coefficient),float(Exponent)
                    Potential[j]+=Coefficient*x[j]**Exponent
                else:
                    Potential[j]+=float(Custom_Function[i])
    elif "STEP" in Input:
        print("Do you want to customize the step function? Default is 0 in case x<0, 1 if x>0")
        Input=input().upper()
        if Input=="N" in Input or Input=="":
            for i in x:
                if i>0:
                    Potential.append(1)
                else:
                    Potential.append(0)
        else:
            print("Please enter the desired amplitude")
            Amplitude=float(input())
            print("Please enter where you want the step to happen")
            Wherestep=float(input())
            for i in x:
                if i>Wherestep:
                    Potential.append(Amplitude)
                else:
                    Potential.append(0)
    elif "QUANTUM HARMONIC OSCILLATOR" in Input or "HARMONIC OSCILLATOR" in Input or "OSCILLATOR" in Input or "QHO" in Input:
        for i in x:
            Potential.append(i**2)
    #
    return Potential


#Testing that potential comes out as desired
import matplotlib.pyplot as plt
import numpy as np
x=np.linspace(-1,1)
plt.plot(x,User_Defined_Potential(x))