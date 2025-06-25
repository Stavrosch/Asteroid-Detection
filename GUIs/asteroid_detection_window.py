import tkinter as tk
from tkinter import filedialog
import Utilities as ut
from astropy.visualization.mpl_normalize import ImageNormalize
import os
from tkinter import ttk
import customtkinter as ctk

def show_progress_and_run(parent_window,pltfrm,image_path,threshold):

    progs_win=ctk.CTkToplevel(parent_window)
    progs_win.title("Processing...")
    progs_win.geometry("300x100")

    progs_lbl=ctk.CTkLabel(progs_win,text="Running detection...")
    progs_lbl.pack(pady=10)

    progs_bar=ttk.Progressbar(progs_win,orient="horizontal",length=200,mode="determinate")
    progs_bar.pack(pady=10)
    ut.detector(progs_bar,progs_lbl,progs_win,image_path ,threshold,pltfrm)


def choose_file(window,threshold,pltfrm):
    global filepth
    filepth=filedialog.askopenfilename(
        filetypes=[("FITS Files","*.fits"),("All Files","*.*")],
        title="Select a FITS file"
    )
    if filepth:
        filenm=os.path.basename(filepth)
        filelbl.configure(text=f"Selected File: {filenm}",text_color="green")
        start.configure(state=ctk.NORMAL)

    else:
        filelbl.configure(text="No file selected",text_color="red")
        start.configure(state=ctk.DISABLED)

def create_window(parent):
    winast=ctk.CTkToplevel(parent)
    winast.title("Asteroid Detection Window")
    winast.geometry("1000x800")

    filefrm=ctk.CTkFrame(winast)
    filefrm.pack(pady=10)
    selectlbl=ctk.CTkLabel(filefrm,text="Select a FITS file for analysis")
    selectlbl.pack(side=ctk.LEFT,padx=5)

    buton1=ctk.CTkButton(filefrm,text="Choose File",command=lambda: choose_file(winast,magsldr.get(),pltfrm))
    buton1.pack(side=ctk.LEFT,padx=5)

    global filelbl
    filelbl=ctk.CTkLabel(winast,text="No file selected",text_color="blue")
    filelbl.pack(pady=2)

    sldrfrm=ctk.CTkFrame(winast)
    sldrfrm.pack(pady=2)

    global magsldr
    maglb=ctk.CTkLabel(sldrfrm,text="Select Magnitude Threshold (for filtering stars):")
    maglb.pack(side=ctk.LEFT,padx=5)

    magsldr=ctk.CTkSlider(sldrfrm,from_=0.002,to=0.04,number_of_steps=19)
    magsldr.set(0.01)
    magsldr.pack(side=ctk.LEFT,padx=5)

    global start
    start=ctk.CTkButton(winast,text="Run Detection",state=ctk.DISABLED,command=lambda: show_progress_and_run(winast,pltfrm,filepth,magsldr.get()))
    start.pack(anchor='n',pady=2)

    plt_lbl=ctk.CTkLabel(winast,text=f"Asteroid Detection",font=("Helvetica",18))
    plt_lbl.pack(anchor='n',pady=0)

    pltfrm=ctk.CTkFrame(winast)
    pltfrm.pack(fill=ctk.BOTH,expand=True)