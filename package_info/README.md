# Schrodinger Equation Simulator

This software package provides a command-line tool that can be used to simulate the Time-Independent Schrodinger Equation for an input potential function.

Features
--------

There are inbuilt functions which can be selected, or the user can input a custom potential function.
The inbuilt functions are:
* Barrier
* Square Well
* Step

A Graphical User Interface is used for this selection/input process, which also allows the user to customise the function parameters. It then shows a GIF of the resulting simulation.


Installation
------------

Launch the GUI via the command line by entering the following instructions:

`$ git clone https://github.com/Irwin-Blair/Group-F`

`$ cd Group-F`

`$ pip install -r requirements.txt`

Additionally,
IF running on Windows:

`pip install tkinter`

`pip install PIL`

IF running on Windows Subsystem for Linux:

`pip install tk`

`pip install pillow`

THEN run 

`$ python ./GUI_Simulation.py`
  
  
Credit
------

Source Code: https://github.com/Irwin-Blair/Group-F

Authors: Irwin Blair, Iarla Boyce, Becca Mallett, Ciar Moore-Saxton, Adam Proctor-Lowe, Robert Wade

This software is licensed under the MIT license.