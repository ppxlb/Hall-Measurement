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
from RESIST import resistivity
from HALL import Hall
from MAGNET import mag

a = set_up()
initialise(a,100)

"""----------GUI SETUP---------"""
window = tk.Tk()
Ilabel = tk.Label(window, text="Current (uA):")#.grid(row=1,column=0)
Ilabel.place(x=20,y=30,width=120,height=25)
I_ent = tk.Entry(window)#.grid(row=1, column=1)
I_ent.delete(0,tk.END)
I_ent.insert(0,"100")
I_ent.place(x=150,y=30,width=120,height=25)
Nlabel = tk.Label(window, text="Sampling Count:")#.grid(row=2,column=0)
Nlabel.place(x=20,y=60,width=120,height=25)
N_ent = tk.Entry(window)#.grid(row=2, column=1)
N_ent.delete(0,tk.END)
N_ent.insert(0,"3")
N_ent.place(x=150,y=60,width=120,height=25)
tlabel = tk.Label(window,text="Thickness (um):")#.grid(row=3,column=0)
tlabel.place(x=20,y=90,width=120,height=25)
t_ent = tk.Entry(window)#.grid(row=3, column=1)
t_ent.delete(0,tk.END)
t_ent.insert(0,"5")
t_ent.place(x=150,y=90,width=120,height=25)
terlabel=tk.Label(window,text="Thickness error (um):")#.grid(row=4,column=0)
terlabel.place(x=20,y=120,width=120,height=25)
ter_ent = tk.Entry(window)#.grid(row=4, column=1)
ter_ent.delete(0,tk.END)
ter_ent.insert(0,"0.5")
ter_ent.place(x=150,y=120,width=120,height=25)

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70)
Txt.place(x=388, y=30)
 
dline = "--------------------------------------------------"

#cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
#cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]])
#cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    
chck_btn = tk.Button(window, text = "Check contacts", command = lambda : chck(meas, avg, a, dline, Txt, tk))
chck_btn.place(x=118,y=200,width = 125,height=45)
shres_btn = tk.Button(window, text = "Resistivity Measurement", command = lambda : resistivity(a, meas_vdp, avg, gain, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), float(tk.Entry.get(ter_ent)), Txt, tk,float(tk.Entry.get(I_ent))))
shres_btn.place(x=118,y=250,width = 125,height=45)
mob_btn = tk.Button(window, text = "Hall Measurement", command = lambda : Hall(a, gain, meas_vdp, avg, R, int(tk.Entry.get(N_ent)), dline, float(tk.Entry.get(t_ent)), float(tk.Entry.get(ter_ent)), Txt, tk, float(tk.Entry.get(I_ent))))
mob_btn.place(x=118,y=300,width = 125,height=45)
mag_btn = tk.Button(window, text = "Reset Magnet", command = lambda : mag(a))
mag_btn.place(x=118,y=350,width=125,height = 45)
window.title("HALL 9000")
window.geometry("900x745+30+30")
window.wm_iconbitmap("HALL9000.ico")
window.mainloop()
