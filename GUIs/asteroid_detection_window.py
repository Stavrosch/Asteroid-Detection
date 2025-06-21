import tkinter as tk
from tkinter import filedialog
import Utilities as ut
from astropy.visualization.mpl_normalize import ImageNormalize
import os
from tkinter import ttk

def show_progress_and_run(parent_window,pltfrm,image_path,threshold):

    progs_win=tk.Toplevel(parent_window)
    progs_win.title("Processing...")
    progs_win.geometry("300x100")

    progs_lbl=tk.Label(progs_win,text="Running detection...")
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
        filelbl.config(text=f"Selected File: {filenm}",fg="green")
        start.config(state=tk.NORMAL)

    else:
        filelbl.config(text="No file selected",fg="red")
        start.config(state=tk.DISABLED)

def create_window(parent):
    winast=tk.Toplevel(parent)
    winast.title("Asteroid Detection Window")
    winast.geometry("1000x800")

    filefrm=tk.Frame(winast)
    filefrm.pack(pady=10)
    selectlbl=tk.Label(filefrm,text="Select a FITS file for analysis")
    selectlbl.pack(side=tk.LEFT,padx=5)

    buton1=tk.Button(filefrm,text="Choose File",command=lambda: choose_file(winast,magsldr.get(),pltfrm))
    buton1.pack(side=tk.LEFT,padx=5)

    global filelbl
    filelbl=tk.Label(winast,text="No file selected",fg="blue")
    filelbl.pack(pady=2)

    sldrfrm=tk.Frame(winast)
    sldrfrm.pack(pady=2)

    maglb=tk.Label(sldrfrm,text="Select Magnitude Threshold (for filtering stars):")
    maglb.pack(side=tk.LEFT,padx=5)

    magsldr=tk.Scale(sldrfrm,from_=0.002,to=0.04,orient=tk.HORIZONTAL,length=100,resolution=0.002)
    magsldr.set(0.01)
    magsldr.pack(side=tk.LEFT,padx=5)

    global start
    start=tk.Button(winast,text="Run Detection",state=tk.DISABLED,command=lambda: show_progress_and_run(winast,pltfrm,filepth,magsldr.get()))
    start.pack(anchor='n',pady=2)

    plt_lbl=tk.Label(winast,text=f"Asteroid Detection",font=("Helvetica",18))
    plt_lbl.pack(anchor='n',pady=0)

    pltfrm=tk.Frame(winast)
    pltfrm.pack(fill=tk.BOTH,expand=True)