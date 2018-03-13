# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 11:17:03 2018

@author: localadmin
"""


def clear(Txt,tk):
    """
    short function that clears the text in the results text box so you don't 
    have to highlight and delete
    """
    Txt.delete('1.0', tk.END)