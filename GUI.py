import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
window = tk.Tk()
window.title('Schrodinger Equation Sim')
window.geometry('600x400')

def ClearWindow():
    for widget in window.winfo_children():
            widget.destroy()
            
def GenImage():
    ClearWindow()
    global x
    im = Image.open("Example.png")
    ph = ImageTk.PhotoImage(im)
    label = tk.Label(image=ph)
    label.grid(row=0,column=0)
    label.image=ph
    labeltext = tk.Label(text="This is your potential function. Do you want to simulate Schrodinger's equation?")
    labeltext.grid(row=1,column=0)
    buttonno=tk.Button(text="No",command=Options,width=25,height=10,background="red")
    buttonno.grid(row=2,column=0)
    buttonyes=tk.Button(text="Yes",command=Schrodinger,width=25,height=10,background="green")
    buttonyes.grid(row=2,column=1)
    
def Schrodinger():
    ClearWindow()
    global x,v_x
    Label=tk.Label(text=(x,v_x))
    Label.pack()
    
def Step():
    ClearWindow()
    def Def_Vals():
        global Wherestep,Upper_Amplitude,Lower_Amplitude
        Wherestep=X_max/2
        Upper_Amplitude=1
        Lower_Amplitude=0
        StepImage()
    Question=tk.Label(text="Do you want to customize where the step occurs?")
    Question.pack()
    yes=tk.Button(text="yes",command=StepCustom,background="Green")
    no=tk.Button(text="no",command=Def_Vals,background="Red")
    yes.pack()
    no.pack()
    
def StepCustom():
    ClearWindow()
    Where=tk.Scale(from_=X_min,to=X_max,orient="horizontal",resolution=0.001*(X_max-X_min))
    Where.pack()
    def Use_Vals():
        global Wherestep,Upper_Amplitude,Lower_Amplitude
        Wherestep=Where.get()
        try:
            Upper_Amplitude=float(Upper.get())
        except:
            Upper_Amplitude=1
        try:
            Lower_Amplitude=float(Lower.get())
        except:
            Lower_Amplitude=0
        StepImage()
    yes=tk.Button(command=Use_Vals,text="Press to generate step function")
    Upper=tk.Entry()
    Lower=tk.Entry()
    Upper.pack()
    Lower.pack()
    yes.pack()
    
def StepImage():
    global v_x
    v_x=np.zeros(len(x))
    for i in range(len(x)):
        if x[i]>Wherestep:
            v_x[i]=Upper_Amplitude
        else:
            v_x[i]=Lower_Amplitude
    plt.plot(x,v_x)
    plt.savefig("Example")
    plt.show()
    GenImage()
    
def Custom(SuppressMessage=True):
    def get_Custom_input():
        global Equation,v_x,Check
        Custom_Input=Equation.get().upper()
        Custom_Function=Custom_Input.split("+")
        v_x=np.zeros(len(x))
        try:
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
                            v_x[j]+=Coefficient*x[j]**Exponent
                        else:
                            #Checking that in case the user gave a constant, therefore no X, we can add that.
                            v_x[j]+=float(Custom_Function[i])
            Check=True
        except:
            ClearWindow()
            Custom(SuppressMessage=False)
            Check=False
        if Check is True:
            plt.plot(x,v_x)
            plt.savefig("Example")
            plt.show()            
            GenImage()
    ClearWindow()
    Welcome = tk.Label(text="Please enter your custom equation")
    Welcome.pack()
    global Equation,v_x,x
    Equation = tk.Entry()
    Equation.pack()
    Button=tk.Button(text="Use my custom function!",command=get_Custom_input)
    Button.pack()
    if SuppressMessage is False:
        Message=tk.Label(text="Sorry, that equation didn't work. Please try again.")
        Message.pack()
    
def Main():
    global X_min
    global X_max
    X_max,X_min="",""
    ClearWindow()
    greeting = tk.Label(text="Please enter the type of potential you would like to simulate.")
    greeting.grid(row=0,column=0)
    button_xvalues = tk.Button(
        text="Submit x-values",
        width=25,
        height=5,
        command=Options
    )
    button_xvalues.grid(row=1,column=0)
    global entryxmin
    global entryxmax
    entryxmin=tk.Entry(width=25)
    entryxmax=tk.Entry(width=25)
    entryxmin.grid(row=2,column=0)
    entryxmax.grid(row=2,column=1)
    
def Options():
    Check=True
    global X_min
    global X_max
    if X_min=="":
        try:
            X_max=float(entryxmax.get())
            print("Check")
            X_min=float(entryxmin.get())
        except:
            Check=False
    ClearWindow()
    if Check is False:
        Warning_X=tk.Label(text="Warning, x-values weren't given as numbers. Using X_min of 0 and X_max=5.")
        X_min=0
        X_max=5
        Warning_X.grid(row=3,column=0)
    global x
    x=np.linspace(X_min,X_max,num=round(100*X_max-X_min))
        
        
    greeting = tk.Label(text="Please enter the type of potential you would like to simulate.")
    greeting.grid(row=0,column=0)
    button_step = tk.Button(
        text="Step function",
        width=25,
        height=5,
        command=Step
    )
    button_custom = tk.Button(
        text="Custom function",
        width=25,
        height=5,
        command=Custom
    )
    button_step.grid(row=1,column=0)
    button_custom.grid(row=1,column=1)
    button_Main = tk.Button(text="Return to the start",width=50,height=5,command=Main)
    button_Main.grid(row=2,column=0)
Main()
window.mainloop()
