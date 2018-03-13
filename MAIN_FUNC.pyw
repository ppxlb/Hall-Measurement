# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

"""-------Import GUI module tkinter and bespoke functions (ALLCAPS)--------"""
import tkinter as tk
from SETUP import set_up
from INITIAL import initialise
from GAIN import gain
from MEAS import meas, meas_vdp
from PROCESS import avg, R
from CHCK import chck
from RESIST import resist, ivity, reivity
from HALL import hall, bulk, rebulk
from MAGNET import mag
from SAVE import save
from CLEAR import clear

a = set_up() #set up instrument addresses with pyvisa module
initialise(a,100) #initialise the instrument and sent a default current of 100uA

"""----------GUI SETUP---------"""
window = tk.Tk() #create instance of our main window

"""Parameter Entry"""
Ilabel = tk.Label(window, text="Current (uA):") #create label for curr entry
Ilabel.place(x=20,y=30,width=120,height=25) #assign place
I_ent = tk.Entry(window) #entry box for curr
I_ent.delete(0,tk.END) #clear entry box
I_ent.insert(0,"100") #set entry box default to 100uA
I_ent.place(x=150,y=30,width=120,height=25) #assign place

Nlabel = tk.Label(window, text="Sampling Count:") #create label for sampling count entry
Nlabel.place(x=20,y=60,width=120,height=25) #assign place
N_ent = tk.Entry(window) #entry box for sampling count
N_ent.delete(0,tk.END) #clear entry box
N_ent.insert(0,"3") #set default entry value as 3
N_ent.place(x=150,y=60,width=120,height=25) #assign place

tlabel = tk.Label(window,text="Thickness (um):") #create label for thickness entry
tlabel.place(x=20,y=90,width=120,height=25) #assign place
t_ent = tk.Entry(window) #create entry box for thickness
t_ent.delete(0,tk.END) #clear entry box
t_ent.insert(0,"5") #set default thickness as 5um
t_ent.place(x=150,y=90,width=120,height=25) #assign place


smpllabel=tk.Label(window,text="Sample Name:") #create label for sample name entry
smpllabel.place(x=20,y=120,width=120,height=25) #assign place
smpl_ent = tk.Entry(window) #create blank entry box for sample name
smpl_ent.place(x=150,y=120,width=120,height=25) #assign place

"""Menu toolbar"""
menubar = tk.Menu(window) #create main menu and assign to menubar
filmenu = tk.Menu(menubar,tearoff=0) #create File Menu and assign to filmenu
filmenu.add_command(label="Save", command = lambda : save(tk.Entry.get(smpl_ent),float(tk.Entry.get(I_ent)),float(tk.Entry.get(t_ent)),dline,Txt,tk)) #assign save function to filmenu
filmenu.add_command(label="Exit", command=window.quit) #assign exit function to filmenu
tolmenu = tk.Menu(menubar,tearoff=0) #create tool menu and assign to tolmenu
tolmenu.add_command(label="Recalculate resistivity", command = lambda : reivity(ivity,float(tk.Entry.get(t_ent)),dline,Txt,tk)) #assign function to recaluclate thickness dependent resistivity
tolmenu.add_command(label="Recalculate Hall values", command = lambda : rebulk(bulk,float(tk.Entry.get(t_ent)),dline,Txt,tk)) #assign function to recalculate Carrier Concentration and Hall coefficient
tolmenu.add_command(label="Reset magnet", command = lambda : mag(a)) #menu option to reset magnet
tolmenu.add_command(label="Clear all text", command = lambda : clear(Txt,tk) ) #menu option to clear all text
menubar.add_cascade(label="File", menu=filmenu) #add menus to menubar
menubar.add_cascade(label="Tools", menu=tolmenu)

"""Text display box"""
scrollbar = tk.Scrollbar(window) #add scrollbar to the window
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #pack to the hard right hand side
Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70) #create results text box and assign scrollbar to it's Y axis
Txt.place(x=388, y=30) #assign place
 
dline = "--------------------------------------------------" #general line break string


"""User Controls"""
    
chck_btn = tk.Button(window, text = "Check contacts", command = lambda : chck(meas, avg, a, dline, Txt, tk)) #button to run a contact check
chck_btn.place(x=118,y=300,width = 140,height=45) #assign place
shres_btn = tk.Button(window, text = "Resistivity Measurement", command = lambda : resist(a, meas_vdp, avg, gain, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), Txt, tk,float(tk.Entry.get(I_ent)))) #button to run resistivity measurements
shres_btn.place(x=118,y=375,width = 140,height=45) #assign place
mob_btn = tk.Button(window, text = "Hall Measurement", command = lambda : hall(a, gain, meas_vdp, avg, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), Txt, tk, float(tk.Entry.get(I_ent)))) #button to run hall measurements and produce results
mob_btn.place(x=118,y=450,width = 140,height=45) #assign place

#mag_btn = tk.Button(window, text = "Reset Magnet", command = lambda : mag(a))
#mag_btn.place(x=118,y=525,width=140,height = 45)
#sav_btn=tk.Button(window,text ="Save",command = lambda : save(tk.Entry.get(smpl_ent),Txt,tk))
#sav_btn.place(x=118,y=600,width=140,height=45)

"""Display Window"""
window.config(menu=menubar) #add in the menubar
window.title("HALL 9000") #name window
window.geometry("1000x800+30+30") #set height and width of window plus a buffer
window.wm_iconbitmap("HALL9000.ico") #set novelty HAL icon
window.mainloop() #execute GUI

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
#fillabel=tk.Label(window,text="file name")
#fillabel.place(x=20,y=675,width=120,height=25)
#fil_ent = tk.Entry(window)
#fil_ent.place(x=150,y=675,width=120,height=25)

#cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
#cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]])
#cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])

#terlabel=tk.Label(window,text="Thickness error (um):")
#terlabel.place(x=20,y=120,width=120,height=25)
#ter_ent = tk.Entry(window)
#ter_ent.delete(0,tk.END)
#ter_ent.insert(0,"0.5")
#ter_ent.place(x=150,y=120,width=120,height=25)