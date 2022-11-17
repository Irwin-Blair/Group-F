#Importing requirements
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from itertools import count, cycle
from findiff import FinDiff
from scipy.sparse.linalg import inv
from scipy.sparse import eye, diags
import matplotlib.animation as animation

def Simulation(x_array,v_x,wave_placement,FgColour,BgColour):
    """Solves schrodinger's equation in 1 Dimension.
    x,v_x should be given as arrays with the same dimensions
    wave_placement should be given as a float between Max(x) and Min(x)
    FgColour,BgColour should be given as strings of colours, eg, black and white."""
    plt.rcParams["axes.labelsize"] = 16

    # Input parameters
    Nx = len(x)

    
    Nt = 250
    tmin = 0
    tmax = 20
    k = 1 
    
    # Calculate grid, potential, and initial wave function
    t_array = np.linspace(tmin, tmax, Nt)
    psi = np.exp(-(x_array - wave_placement)**2)
    
    # Calculate finite difference elements
    dt = t_array[1] - t_array[0]
    dx = x_array[1] - x_array[0]
    
    # Convert to a diagonal matrix
    v_x_matrix = diags(v_x)
    
    # Calculate the Hamiltonian matrix
    H = -0.5 * FinDiff(0, dx, 2).matrix(x_array.shape) + v_x_matrix
    
    # Apply boundary conditions to the Hamiltonian
    H[0, :] = H[-1, :] = 0
    H[0, 0] = H[-1, -1] = 1
    
    # Calculate U
    I_plus = eye(Nx) + 1j * dt / 2. * H
    I_minus = eye(Nx) - 1j * dt / 2. * H
    U = inv(I_minus).dot(I_plus)
    
    # Iterate over each time, appending each calculation of psi to a list
    psi_list = []
    for t in t_array:
        psi = U.dot(psi)
        psi[0] = psi[-1] = 0
        psi_list.append(np.abs(psi))
        
    psi_mag_squared = np.abs(psi_list)**2
    
    
    fig, ax = plt.subplots()
    #Styling the fit
    ax.set_xlabel("x [arb units]")
    ax.set_ylabel("$|\Psi(x, t)|^2$", color="C0")
    #Making the fit work with darkmode
    fig.patch.set_facecolor(BgColour)
    ax.patch.set_facecolor(BgColour)
    ax.xaxis.label.set_color(FgColour)
    ax.tick_params(axis='x', colors=FgColour)
    ax.tick_params(axis='y', colors=FgColour)
    ax.spines['left'].set_color(FgColour)
    ax.spines['top'].set_color(FgColour)
    ax.spines['right'].set_color(FgColour)
    ax.spines['bottom'].set_color(FgColour)
    ax.grid(color=FgColour)
    
    ax_twin = ax.twinx()
    ax_twin.tick_params(axis='y', colors=FgColour)
    ax_twin.plot(x_array, v_x, color="C1")
    ax_twin.set_ylabel("V(x) [arb units]", color="C1")
    
    line, = ax.plot([], [], color="C0", lw=2)
    xdata, ydata = [], []
    
    def run(psi):
        line.set_data(x_array, np.abs(psi)**2)
        return line,
    
    ax.set_xlim(x_array[0], x_array[-1])
    ax.set_ylim(0, 1)
    
    ani = animation.FuncAnimation(fig, run, psi_list, interval=10)
    ani.save("Assets/Simulation.gif", fps=120)
    
#Setting up initial tkinter window, default is lightmode
window = tk.Tk()
BgColour="White"
FgColour="Black"
Darkmode=False
dmtext="Enable darkmode?"
window["bg"]=BgColour
window.title('Schrodinger Equation Sim')
window.geometry('600x400')

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        #try:
            #self.delay = im.info['duration']
        #except:
        self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

def ClearWindow():
    """Clears the currently displayed window.
    Takes no arguments and doesn't return anything"""
    for widget in window.winfo_children():
            widget.destroy()
            
def GenImage():
    """Using a global x,v_x varible, this creates a graph of v_x against x, and displays it on a window. Asks the user if they want to simulate schrodinger's equation. 
    Takes no arguments and doesn't return anything"""
    global x,v_x
    #Generating the figure
    fig=plt.figure()
    ax=fig.add_subplot()
    #Making figure match the animation in style
    plt.plot(x,v_x,color="C1")
    ax.set_xlabel("x [arb units]")
    ax.set_ylabel("V(x) [arb units]", color="C1")
    #Making graph fit with darkmode
    fig.patch.set_facecolor(BgColour)
    ax.patch.set_facecolor(BgColour)
    ax.xaxis.label.set_color(FgColour)
    ax.tick_params(axis='x', colors=FgColour)
    ax.tick_params(axis='y', colors=FgColour)
    ax.spines['left'].set_color(FgColour)
    ax.spines['top'].set_color(FgColour)
    ax.spines['right'].set_color(FgColour)
    ax.spines['bottom'].set_color(FgColour)
    ax.grid(color=FgColour)
    #Saving the figure
    plt.savefig("Assets/Demonstration.png")
    ClearWindow()
    #Configuring the window to make information more readable
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1,2),weight=1)
    #Displaying the image
    im = Image.open("Assets/Demonstration.png")
    ph = ImageTk.PhotoImage(im)
    label = tk.Label(image=ph)
    label.grid(row=0,columnspan=2)
    label.image=ph
    #Displaying text and buttons underneath the plot
    labeltext = tk.Label(fg=FgColour,bg=BgColour,text="This is your potential function. Do you want to simulate Schrodinger's equation?")
    labeltext.grid(row=1,columnspan=2)
    buttonno=tk.Button(text="No",command=Options,width=15,height=7,background="red")
    buttonno.grid(row=2,column=1)
    buttonyes=tk.Button(text="Yes",command=Schrodinger,width=15,height=7,background="green")
    buttonyes.grid(row=2,column=0)
    
def Schrodinger(Check=False,InitialX=0):
    """Displays an image of the potential if Check is False, otherwise shows a simulation animation of the wavefunction with it starting at InitialX
    Check = Boolean
    Initial X = float
    """
    ClearWindow()
    #Configuring the window to make information more readable
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1,2),weight=1)
    #Displaying the slider and text to determine the initial position of x
    InitialText=tk.Label(bg=BgColour,fg=FgColour,text="Please enter the initial position of the wavefunction.")
    InitialText.grid(row=0,column=0)
    Initial=tk.Scale(bg=BgColour,fg=FgColour,from_=X_min,to=X_max,orient="horizontal",resolution=0.001*(X_max-X_min))
    Initial.grid(row=0,column=1)
    def SIMULATE(Initialx=Initial):
        """Is called with a button and cannot be given non default arguements. Plots the animation of schrodinger's equation."""
        #Getting the value for inital x from the slider
        Initial=Initialx.get()
        Schrodinger(Check=True,InitialX=Initial)
    #Buttons for determining whether or not to Simulate the wavefunction or return to the options
    Button=tk.Button(text="Simulate",background="Green",command=SIMULATE)
    Button.grid(row=1,column=0)
    buttonoptions=tk.Button(text="Return to options",command=Options,background="red")
    buttonoptions.grid(row=1,column=1)
    #Checks if the user has clicked Simulate
    if Check is False:
        im = Image.open("Assets/Demonstration.png")
        ph = ImageTk.PhotoImage(im)
        label = tk.Label(image=ph)
        label.grid(row=2,columnspan=2)
        label.image=ph
    else:
        Simulation(x,v_x,InitialX,FgColour,BgColour)
        label = ImageLabel()
        label.grid(row=2,columnspan=2)
        label.load('Assets/Simulation.gif')
        
    
def Step():
    """Initial page for asking if user wants to customize chosen function.
    Takes no arguments and doesn't return anything"""
    ClearWindow()
    #Configuring the window to make information more readable
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1),weight=1)
    #If the user doesn't want to customize, the program uses these default values, and calls StepImage
    def Def_Vals():
        global Wherestep,Upper_Amplitude,Lower_Amplitude
        Wherestep=(X_max+X_min)/2
        Upper_Amplitude=1
        Lower_Amplitude=0
        StepImage()
    #Placing the choice buttons on the window
    Question=tk.Label(bg=BgColour,fg=FgColour,text="Do you want to customize where the step occurs?")
    Question.grid(row=0,columnspan=2)
    yes=tk.Button(bg=BgColour,fg=FgColour,text="Yes",command=StepCustom,background="Green",width=23,height=10)
    no=tk.Button(bg=BgColour,fg=FgColour,text="No",command=Def_Vals,background="Red",width=23,height=10)
    yes.grid(row=1,column=0)
    no.grid(row=1,column=1)
    
def StepCustom():
    """Initial page for user customizing the chosen function.
    Takes no arguments and doesn't return anything"""
    ClearWindow()
    WhereText=tk.Label(bg=BgColour,fg=FgColour,text="Where do you want the step to occur?")
    Where=tk.Scale(bg=BgColour,fg=FgColour,from_=X_min,to=X_max,orient="horizontal",resolution=0.001*(X_max-X_min))
    Where.grid(row=0,column=1)
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
    yes=tk.Button(bg=BgColour,fg=FgColour,command=Use_Vals,text="Press to generate step function")
    Upper=tk.Entry(bg=BgColour,fg=FgColour)
    Lower=tk.Entry(bg=BgColour,fg=FgColour)
    LowerText=tk.Label(bg=BgColour,fg=FgColour,text="What do you want the lower amplitude of the step function to be?")
    UpperText=tk.Label(bg=BgColour,fg=FgColour,text="What do you want the upper amplitude of the step function to be?")
    WhereText.grid(row=0,column=0)
    UpperText.grid(row=1,column=0)
    LowerText.grid(row=2,column=0)
    Upper.grid(row=1,column=1)
    Lower.grid(row=2,column=1)
    yes.grid(row=3)
    
def StepImage():
    """Takes x and transforms it into the chosen v_x, then calls GenImage"""
    global v_x
    v_x=np.zeros(len(x))
    for i in range(len(x)):
        if x[i]>Wherestep:
            v_x[i]=Upper_Amplitude
        else:
            v_x[i]=Lower_Amplitude
    GenImage()
    
def Custom(SuppressMessage=True):
    """Initial page for user customizing the chosen function.
    SuppressMessage should be a boolean. If SuppressMessage is False, displays a warning message"""
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1,2),weight=1)
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
            GenImage()
    ClearWindow()
    Welcome = tk.Label(text="Please enter your custom equation in the entry field below.",bg=BgColour,fg=FgColour)
    Welcome.grid(row=0,columnspan=2)
    global Equation,v_x,x
    Equation = tk.Entry(bg=BgColour,fg=FgColour)
    Equation.grid(row=1,column=0)
    Button=tk.Button(text="Use my custom function!",command=get_Custom_input,bg=BgColour,fg=FgColour)
    Button.grid(row=1,column=1)
    if SuppressMessage is False:
        Message=tk.Label(text="Sorry, that equation didn't work. Please try again.",bg=BgColour,fg=FgColour)
        Message.grid(row=2,columnspan=2)
        
def Barrier():
    """Initial page for asking if user wants to customize chosen function.
    Takes no arguments and doesn't return anything"""
    ClearWindow()
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1),weight=1)
    def Def_Vals():
        Wheres=[(X_max+X_min)/2]
        Amplitudes=[1]
        Widths=[(np.abs(X_max)+np.abs(X_min))/10]
        BarrierImage(Wheres,Amplitudes,Widths)
    Question=tk.Label(bg=BgColour,fg=FgColour,text="Do you want to customize the barriers?")
    Question.grid(row=0,columnspan=2)
    yes=tk.Button(bg=BgColour,fg=FgColour,text="Yes",command=BarrierCustom,background="Green",width=23,height=10)
    no=tk.Button(bg=BgColour,fg=FgColour,text="No",command=Def_Vals,background="Red",width=23,height=10)
    yes.grid(row=1,column=0)
    no.grid(row=1,column=1)
    
def BarrierCustom(Num=0,SuppressMessage=False):
    """Initial page for user customizing the chosen function.
    Num should be an integer, and SuppressMessage a boolean. If SuppressMessage is True, displays a warning message, and if Num!=0 it displays Num configureable barriers"""
    ClearWindow()
    RowIndex=[]
    for i in range(2*Num+2):
        RowIndex.append(i)
    if SuppressMessage is True:
        InvalidValue=tk.Label(bg=BgColour,fg=FgColour,text="Sorry, that value couldn't be used. Please use integers.")
        InvalidValue.grid(row=1,columnspan=3)
    window.grid_columnconfigure((0,1,2), weight=1)
    window.grid_rowconfigure((0,1),weight=1)
    HowManyText=tk.Label(bg=BgColour,fg=FgColour,text="How many barriers would you like?")
    HowMany=tk.Entry(bg=BgColour,fg=FgColour)
    def HowManyFunc(HowMany=HowMany):
        """Gets how many barriers the user wants from the entry field HowMany."""
        try:
            Num=np.abs(int(HowMany.get()))
            BarrierCustom(Num=Num)
        except:
            BarrierCustom(SuppressMessage=True)
    HowManyButton=tk.Button(bg=BgColour,fg=FgColour,command=HowManyFunc,text="Press to confirm how many barriers")
    HowManyText.grid(row=0,column=0)
    HowMany.grid(row=0,column=1)
    HowManyButton.grid(row=0,column=2)
    if Num!=0 and SuppressMessage is False:
        window.grid_rowconfigure(tuple(RowIndex),weight=1)
        Wheres,Widths,Amplitudes=[],[],[]
        for i in range(Num):
            if i+1==1:
                EndStr="st"
            elif i+1==2:
                EndStr="nd"
            elif i+1==3:
                EndStr="rd"
            else:
                EndStr="th"
            LabelWhere=tk.Label(bg=BgColour,fg=FgColour,text=f"Where do you want the {i+1}{EndStr} barrier to be?")
            LabelWhere.grid(row=1+2*i,column=0)
            Where=tk.Scale(bg=BgColour,fg=FgColour,from_=X_min,to=X_max,orient="horizontal",resolution=0.001*(X_max-X_min))
            Where.grid(row=1+2*i,column=1)
            Wheres.append(Where)
            LabelWidth=tk.Label(bg=BgColour,fg=FgColour,text="How wide do you want it to be?")
            LabelWidth.grid(row=2+2*i,column=0)
            Width=tk.Scale(bg=BgColour,fg=FgColour,from_=0,to=(np.abs(X_max)+np.abs(X_min)),orient="horizontal",resolution=0.001*(X_max-X_min))
            Width.grid(row=2+2*i,column=1)
            Widths.append(Width)
            LabelAmplitude=tk.Label(bg=BgColour,fg=FgColour,text="What amplitude do you want this barrier to have?")
            LabelAmplitude.grid(row=1+2*i,column=2)
            Amplitude=tk.Entry(bg=BgColour,fg=FgColour)
            Amplitude.grid(row=2+2*i,column=2)
            Amplitudes.append(Amplitude)
        def Getinfo():
            """Gets the information from the sliders and entry fields. If an entry field has a non float component, sets the amplitude to 0.
            Takes no arguments and doesn't return anything"""
            for i in range(Num):
                Wheres[i],Widths[i]=Wheres[i].get(),Widths[i].get()
                try:
                    Amplitudes[i]=float(Amplitudes[i].get())
                except:
                    Amplitudes[i]=0
            BarrierImage(Wheres,Amplitudes,Widths)
        Button=tk.Button(command=Getinfo,bg=BgColour,fg=FgColour,text="Use these barriers")
        Button.grid(row=Num*2+2)
        
def BarrierImage(Wheres,Amplitudes,Widths):
    """Takes x and transforms it into the chosen v_x, then calls GenImage
    Wheres, Amplitudes and Widths should all be lists of the same dimensions, all containing floats"""
    global v_x
    v_x=np.zeros(len(x))
    for j in range(len(Widths)):
        Width=Widths[j]
        Where=Wheres[j]
        Amplitude=Amplitudes[j]
        for i in range(len(x)):
            if Where-Width/2<x[i]<Where+Width/2:
                if v_x[i]<Amplitude:
                    v_x[i]=Amplitude
    GenImage()
    

def Well():
    """Initial page for asking if user wants to customize chosen function.
    Takes no arguments and doesn't return anything"""
    ClearWindow()
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1),weight=1)
    def Def_Vals():
        global Wherestep,Upper_Amplitude,Lower_Amplitude,Well_Width
        Wherestep=(X_max+X_min)/2
        Upper_Amplitude=1
        Lower_Amplitude=0
        Well_Width=(np.abs(X_max)+np.abs(X_min))/2
        WellImage()
    Question=tk.Label(bg=BgColour,fg=FgColour,text="Do you want to customize where the well occurs?")
    Question.grid(row=0,columnspan=2)
    yes=tk.Button(bg=BgColour,fg=FgColour,text="Yes",command=WellCustom,background="Green",width=23,height=10)
    no=tk.Button(bg=BgColour,fg=FgColour,text="No",command=Def_Vals,background="Red",width=23,height=10)
    yes.grid(row=1,column=0)
    no.grid(row=1,column=1)
    
def WellCustom():
    """Initial page for user customizing the chosen function.
    Takes no arguments and doesn't return anything"""
    ClearWindow()
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1,2,3,4),weight=1)
    WhereText=tk.Label(bg=BgColour,fg=FgColour,text="Where do you want the well to be centered?")
    Where=tk.Scale(bg=BgColour,fg=FgColour,from_=X_min,to=X_max,orient="horizontal",resolution=0.001*(X_max-X_min))
    Where.grid(row=0,column=1)
    WhereText.grid(row=0,column=0)
    WidthText=tk.Label(bg=BgColour,fg=FgColour,text="How wide do you want the well to be?")
    Width=tk.Scale(bg=BgColour,fg=FgColour,from_=0,to=(np.abs(X_max)+np.abs(X_min)),orient="horizontal",resolution=0.001*(X_max-X_min))
    Width.grid(row=1,column=1)
    WidthText.grid(row=1,column=0)
    def Use_Vals():
        global Wherestep,Upper_Amplitude,Lower_Amplitude,Well_Width
        Wherestep=Where.get()
        Well_Width=Width.get()
        try:
            Upper_Amplitude=float(Upper.get())
        except:
            Upper_Amplitude=1
        try:
            Lower_Amplitude=float(Lower.get())
        except:
            Lower_Amplitude=0
        WellImage()
    yes=tk.Button(bg=BgColour,fg=FgColour,command=Use_Vals,text="Press to generate square well")
    Upper=tk.Entry(bg=BgColour,fg=FgColour)
    Lower=tk.Entry(bg=BgColour,fg=FgColour)
    UpperText=tk.Label(bg=BgColour,fg=FgColour,text="Please enter the upper amplitude of the well")
    LowerText=tk.Label(bg=BgColour,fg=FgColour,text="Please enter the lower amplitude of the well")
    Upper.grid(row=2,column=1)
    Lower.grid(row=3,column=1)
    UpperText.grid(row=2,column=0)
    LowerText.grid(row=3,column=0)
    yes.grid(row=4,columnspan=2)

def WellImage():
    """Takes x and transforms it into the chosen v_x, then calls GenImage.
    Takes no arguments and doesn't return anything"""
    global v_x
    v_x=np.zeros(len(x))
    for i in range(len(x)):
        if x[i]>Wherestep+Well_Width/2 or x[i]<Wherestep-Well_Width/2:
            v_x[i]=Upper_Amplitude
        else:
            v_x[i]=Lower_Amplitude
    GenImage()
    
def Main():
    """Initial page for asking if user wants to customize X limits
    Takes no arguments and doesn't return anything"""
    global X_min
    global X_max
    X_max,X_min="",""
    ClearWindow()
    window.grid_columnconfigure((0, 1), weight=1)
    window.grid_rowconfigure((0,1,2,3,4),weight=1)
    greeting = tk.Label(bg=BgColour,fg=FgColour,text="Please enter the upper and lower bounds of x you would like to simulate.")
    greeting.grid(row=0,columnspan=2)
    button_xvalues = tk.Button(bg=BgColour,fg=FgColour,
        text="Submit x limits",
        width=15,
        height=5,
        command=Options
    )
    button_xvalues.grid(row=3,columnspan=2)
    global entryxmin
    global entryxmax
    entryxmin=tk.Entry(bg=BgColour,fg=FgColour,width=25)
    entryxmax=tk.Entry(bg=BgColour,fg=FgColour,width=25)
    MinX=tk.Label(bg=BgColour,fg=FgColour,text="Minimum X")
    MaxX=tk.Label(bg=BgColour,fg=FgColour,text="Maximum X")
    MinX.grid(row=1,column=0)
    MaxX.grid(row=1,column=1)
    entryxmin.grid(row=2,column=0)
    entryxmax.grid(row=2,column=1)
    def Dark():
        """Flips the GUI between darkmode and not darkmode."""
        global Darkmode,BgColour,FgColour,dmtext,Window
        BgColour,FgColour=FgColour,BgColour
        if Darkmode is True:
            dmtext="Enable darkmode?"
            Darkmode=False
            window["bg"]=BgColour
        else:
            Darkmode=True
            window["bg"]=BgColour
            dmtext="Disable darkmode?"
        Main()
            
    button_darkmode = tk.Button(text=dmtext,bg=BgColour,fg=FgColour,command=Dark)
    button_darkmode.grid(row=4,columnspan=2)
    
def Options():
    """Generates a place from which the user can choose their potential function.
    Takes no arguements and returns nothing."""
    window.grid_columnconfigure((0, 1,2), weight=1)
    window.grid_rowconfigure((0,1,2,3,4,5,6),weight=1)
    Check=True
    global X_min
    global X_max
    if X_min=="":
        try:
            X_max=float(entryxmax.get())
            X_min=float(entryxmin.get())
            if X_min>=X_max:
                Check=False
        except:
            Check=False
    ClearWindow()
    if Check is False:
        Warning_X=tk.Label(bg=BgColour,fg=FgColour,text="Warning, x-values weren't given as numbers. Using X_min of -5 and X_max of 5.")
        X_min=-5
        X_max=5
        Warning_X.grid(row=6,columnspan=3)
    global x
    x=np.linspace(X_min,X_max,num=round(100*X_max-X_min))
        
        
    greeting = tk.Label(bg=BgColour,fg=FgColour,text="Please enter the type of potential you would like to simulate.")
    greeting.grid(row=0,columnspan=3)
    button_step = tk.Button(
        bg=BgColour,
        fg=FgColour,
        text="Step function",
        width=15,
        height=2,
        command=Step
    )
    button_custom = tk.Button(
        bg=BgColour,
        fg=FgColour,
        text="Custom function",
        width=15,
        height=2,
        command=Custom
    )
    button_well = tk.Button(
        bg=BgColour,
        fg=FgColour,
        text="Square well function",
        width=15,
        height=2,
        command=Well
    )
    button_barriers = tk.Button(
        bg=BgColour,
        fg=FgColour,
        text="Barrier function",
        width=15,
        height=2,
        command=Barrier
    )
    button_step.grid(row=1,column=1)
    button_barriers.grid(row=2,column=1)
    button_well.grid(row=3,column=1)
    button_custom.grid(row=4,column=1)
    button_Main = tk.Button(bg="red",text="Return to the start",width=20,height=3,command=Main)
    button_Main.grid(row=5,column=1)
Main()
window.mainloop()
