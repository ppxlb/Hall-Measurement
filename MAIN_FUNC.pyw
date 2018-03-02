# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

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

a = set_up()
initialise(a,100)

"""----------GUI SETUP---------"""
window = tk.Tk()

"""Parameter Entry"""
Ilabel = tk.Label(window, text="Current (uA):")
Ilabel.place(x=20,y=30,width=120,height=25)
I_ent = tk.Entry(window)
I_ent.delete(0,tk.END)
I_ent.insert(0,"100")
I_ent.place(x=150,y=30,width=120,height=25)

Nlabel = tk.Label(window, text="Sampling Count:")
Nlabel.place(x=20,y=60,width=120,height=25)
N_ent = tk.Entry(window)
N_ent.delete(0,tk.END)
N_ent.insert(0,"3")
N_ent.place(x=150,y=60,width=120,height=25)

tlabel = tk.Label(window,text="Thickness (um):")
tlabel.place(x=20,y=90,width=120,height=25)
t_ent = tk.Entry(window)
t_ent.delete(0,tk.END)
t_ent.insert(0,"5")
t_ent.place(x=150,y=90,width=120,height=25)

terlabel=tk.Label(window,text="Thickness error (um):")
terlabel.place(x=20,y=120,width=120,height=25)
ter_ent = tk.Entry(window)
ter_ent.delete(0,tk.END)
ter_ent.insert(0,"0.5")
ter_ent.place(x=150,y=120,width=120,height=25)

smpllabel=tk.Label(window,text="Sample Name:")
smpllabel.place(x=20,y=150,width=120,height=25)
smpl_ent = tk.Entry(window)
smpl_ent.place(x=150,y=150,width=120,height=25)

"""Menu toolbar"""
menubar = tk.Menu(window)
filmenu = tk.Menu(menubar,tearoff=0)
filmenu.add_command(label="Save", command = lambda : save(tk.Entry.get(smpl_ent),Txt,tk))
filmenu.add_command(label="Exit", command=window.quit)
edimenu = tk.Menu(menubar,tearoff=0)
edimenu.add_command(label="Recalculate Resistivity", command = lambda : reivity(ivity,float(tk.Entry.get(t_ent)),Txt,tk))
edimenu.add_command(label="Recalculate Mobility", command = lambda : rebulk(bulk,float(tk.Entry.get(t_ent)),Txt,tk))
menubar.add_cascade(label="File", menu=filmenu)
menubar.add_cascade(label="Edit", menu=edimenu)

"""Text display box"""
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70)
Txt.place(x=388, y=30)
 
dline = "--------------------------------------------------"


"""User Controls"""
    
chck_btn = tk.Button(window, text = "Check contacts", command = lambda : chck(meas, avg, a, dline, Txt, tk))
chck_btn.place(x=118,y=300,width = 140,height=45)
shres_btn = tk.Button(window, text = "Resistivity Measurement", command = lambda : resist(a, meas_vdp, avg, gain, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), float(tk.Entry.get(ter_ent)), Txt, tk,float(tk.Entry.get(I_ent))))
shres_btn.place(x=118,y=375,width = 140,height=45)
mob_btn = tk.Button(window, text = "Hall Measurement", command = lambda : hall(a, gain, meas_vdp, avg, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), float(tk.Entry.get(ter_ent)), Txt, tk, float(tk.Entry.get(I_ent))))
mob_btn.place(x=118,y=450,width = 140,height=45)
mag_btn = tk.Button(window, text = "Reset Magnet", command = lambda : mag(a))
mag_btn.place(x=118,y=525,width=140,height = 45)
#sav_btn=tk.Button(window,text ="Save",command = lambda : save(tk.Entry.get(smpl_ent),Txt,tk))
#sav_btn.place(x=118,y=600,width=140,height=45)

"""Display Window"""
window.config(menu=menubar)
window.title("HALL 9000")
window.geometry("1000x800+30+30")
window.wm_iconbitmap("HALL9000.ico")
window.mainloop()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
#fillabel=tk.Label(window,text="file name")
#fillabel.place(x=20,y=675,width=120,height=25)
#fil_ent = tk.Entry(window)
#fil_ent.place(x=150,y=675,width=120,height=25)

#cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
#cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]])
#cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])