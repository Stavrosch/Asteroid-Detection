import tkinter as tk
from tkinter import filedialog
import Utilities as ut
from astropy.visualization.mpl_normalize import ImageNormalize
import os
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import os
from tkinter import StringVar


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BG_COLOR = "#2b2b2b"  
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#1f6aa5"  
HOVER_COLOR = "#144870"  
SLIDER_COLOR = "#3e3e3e"  
DISABLED_COLOR = "#4a4a4a"
ACCENT_COLOR="#4f1ed6"
logo_path = os.path.join(BASE_DIR, 'logowithouttext.png')


def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')  
    
    style.configure("TProgressbar",
                    troughcolor=SLIDER_COLOR,
                    background=ACCENT_COLOR,
                    bordercolor=BG_COLOR,
                    lightcolor=ACCENT_COLOR,
                    darkcolor=ACCENT_COLOR)

def show_progress_and_run(parent_window, pltfrm, image_path, threshold, tree, report_button, ax, fig,console, format_dropdown):
    progs_win = tk.Toplevel(parent_window)
    progs_win.title("Processing...")
    progs_win.geometry("300x100")
    progs_win.configure(bg=BG_COLOR)
    progs_win.resizable(False, False)
    
    progs_win.transient(parent_window)
    progs_win.grab_set()
    
    progs_lbl = tk.Label(progs_win, text="Running detection...", 
                        bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 10))
    progs_lbl.place(relx=0.5, rely=0.3, anchor='center')

    progs_bar = ttk.Progressbar(progs_win, orient="horizontal", 
                              length=200, mode="determinate",
                              style="TProgressbar")
    progs_bar.place(relx=0.5, rely=0.6, anchor='center')
    
    ut.detector(progs_bar, progs_lbl, progs_win, image_path, threshold, pltfrm, BG_COLOR, FG_COLOR, ACCENT_COLOR, HOVER_COLOR, tree, report_button,ax,fig,console, format_dropdown)

def choose_file(window, threshold, pltfrm):
    global filepth
    filepth = filedialog.askopenfilename(
        filetypes=[("FITS Files","*.fits"),("All Files","*.*")],
        title="Select a FITS file"
    )
    if filepth:
        filenm = os.path.basename(filepth)
        filelbl.config(text=f"Selected File: {filenm}", fg="green")
        start.config(state=tk.NORMAL, bg=ACCENT_COLOR)
    else:
        filelbl.config(text="No file selected", fg="red")
        start.config(state=tk.DISABLED)

def create_window(parent):
    import time
    start_time = time.time()
    winast = tk.Toplevel(parent)
    winast.configure(bg=BG_COLOR)
    winast.title("Asteroid Detection Window")
    winast.geometry("1000x800")
    
    logo_img = Image.open(logo_path)
    logo_photo = ImageTk.PhotoImage(logo_img)
    winast.iconphoto(False, logo_photo)
    #winast.attributes('-fullscreen', True)  # Make window fullscreen
    
    # File selection frame
    filefrm = tk.Frame(winast, bg=BG_COLOR)
    filefrm.place(relx=0.02, rely=0.02, relwidth=0.96, height=40)
    
    selectlbl = tk.Label(filefrm, text="Select a FITS file for analysis",   
                    bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 12, 'bold'))
    selectlbl.place(relx=0, rely=0.5, anchor='w')
    
    buton1 = tk.Button(filefrm, text="Choose File", 
                      bg=ACCENT_COLOR, fg=FG_COLOR, 
                      activebackground=HOVER_COLOR,
                      activeforeground=FG_COLOR,
                      relief=tk.FLAT, 
                      font=('Segoe UI', 9),
                      cursor="hand2",
                      command=lambda: choose_file(winast, magsldr.get(), pltfrm))
    buton1.place(relx=0.3, rely=0.5, anchor='w', width=100)
    
    global filelbl
    filelbl = tk.Label(winast, text="No file selected", fg="#2196F3",   
                  bg=BG_COLOR, font=('Segoe UI', 11)) 
    filelbl.place(relx=0.02, rely=0.07, anchor='w')
    
    # Slider frame
    sldrfrm = tk.Frame(winast, bg=BG_COLOR)
    sldrfrm.place(relx=0.02, rely=0.1, relwidth=0.96, height=70)
    
    maglb = tk.Label(sldrfrm, text="Detection Threshold (% of max brightness):",
                    bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 12))
    maglb.place(relx=0, rely=0.3, anchor='w')
    
    magsldr = tk.Scale(sldrfrm, from_=0.002, to=0.04, orient=tk.HORIZONTAL,
                      length=150, resolution=0.002,
                      bg=SLIDER_COLOR, fg=FG_COLOR)
    magsldr.set(0.02)
    magsldr.place(relx=0.35, rely=0.35, anchor='w')
    
    tooltip_text = "This sets the minimum brightness a blob must have to be detected.\n" \
                "For example, 0.03 means 3% of the brightest pixel.\nHigher values = fewer but brighter detections."
    ut.ToolTip(maglb, tooltip_text, 8, FG_COLOR)
    
    global start
    start = tk.Button(
        winast, text="Run Detection",
        bg=DISABLED_COLOR, fg=FG_COLOR, 
        activebackground=HOVER_COLOR,
        activeforeground=FG_COLOR,
        relief=tk.FLAT,
        font=('Segoe UI', 10, 'bold'),
        cursor="hand2",
        state=tk.DISABLED,
        command=lambda: show_progress_and_run(winast, pltfrm, filepth, magsldr.get(), tree, report_button,ax,fig,console, format_dropdown))
    start.place(relx=0.5, rely=0.2, anchor='center', width=120, height=30)
    
    # Main plot frame
    pltfrm = tk.Frame(winast, bg=ACCENT_COLOR)
    pltfrm.place(relx=0.02, rely=0.23, relwidth=0.98, relheight=0.55)
    
    content_frame = tk.Frame(pltfrm, bg=BG_COLOR)
    content_frame.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.98, anchor='center')
    
    fig = Figure(figsize=(5, 5), dpi=100, facecolor=BG_COLOR)
    ax = fig.add_subplot(111)
    ax.set_facecolor(BG_COLOR)
    ax.set_title("No image loaded", fontsize=16, color=FG_COLOR)
    ax.tick_params(colors=FG_COLOR)
    ax.xaxis.label.set_color(FG_COLOR)
    ax.yaxis.label.set_color(FG_COLOR)
    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    
    control_frame = tk.Frame(content_frame, bg=BG_COLOR)
    control_frame.place(relx=0.5, rely=0.95, relwidth=0.98, height=40, anchor='center')
    
    toolbar = NavigationToolbar2Tk(canvas, control_frame)
    toolbar.update()
    toolbar.config(background=BG_COLOR)
    toolbar._message_label.config(background=BG_COLOR, foreground=FG_COLOR)
    
    canvas.get_tk_widget().place(relx=0.5, rely=0.45, relwidth=0.98, relheight=0.9, anchor='center')
    
    result_frame = tk.Frame(winast, bg=BG_COLOR)
    result_frame.place(relx=0.02, rely=0.80, relwidth=0.45, relheight=0.2)
    
    tree_frame = tk.Frame(result_frame, bg=BG_COLOR)
    tree_frame.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.98, anchor='center')
    
    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.place(relx=0.98, rely=0.3, relheight=0.75, anchor='e')
    
    tree = ut.SelectableTreeView(tree_frame, yscrollcommand=tree_scroll.set, selectmode="none")
    tree.place(relx=0, rely=0, relwidth=0.95, relheight=.75)
    tree_scroll.config(command=tree.yview)
    report_button = tk.Button(tree_frame, text="Report", 
                            bg=ACCENT_COLOR, fg=FG_COLOR,
                            activebackground=HOVER_COLOR,
                            relief=tk.FLAT,
                            state=tk.NORMAL)
    report_button.place(relx=0.95, rely=0.87, anchor='e', width=80)
    
    format_var = tk.StringVar(value="80-column")
    # format_frame = tk.Frame(tree_frame, bg=BG_COLOR)
    # format_frame.place(relx=0.75, rely=0.87, anchor='e', width=120)

    # format_label = tk.Label(tree_frame, text="Report Format:", 
    #                     bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 8))
    # format_label.place(relx=0.45, rely=0.87, anchor='e', width=120)

    format_dropdown = ttk.Combobox(tree_frame, textvariable=format_var, 
                                values=["80-column", "ADES"], 
                                state="readonly", width=8)
    format_dropdown.place(relx=0.55, rely=0.87, anchor='e', width=120)

    tree['columns'] = ("X", "Y", "Mag", "RA", "Dec")
    tree.column("#0", width=60)  
    tree.column("X", anchor=tk.CENTER, width=50)
    tree.column("Y", anchor=tk.CENTER, width=50)
    tree.column("Mag", anchor=tk.CENTER, width=60)
    tree.column("RA", anchor=tk.CENTER, width=90)
    tree.column("Dec", anchor=tk.CENTER, width=90) 
    
    tree.heading("#0", text="Selected", anchor=tk.CENTER)
    tree.heading("X", text="X", anchor=tk.CENTER)
    tree.heading("Y", text="Y", anchor=tk.CENTER)
    tree.heading("Mag", text="Mag", anchor=tk.CENTER)
    tree.heading("RA", text="RA", anchor=tk.CENTER)
    tree.heading("Dec", text="Dec", anchor=tk.CENTER)
    print(f"Window created in {time.time() - start_time:.2f} seconds")
    
    console_frame = tk.Frame(winast, bg=BG_COLOR)
    console_frame.place(relx=0.5, rely=0.80, relwidth=0.48, relheight=0.17)

    console = tk.Text(console_frame, bg=BG_COLOR, fg=FG_COLOR, 
                    font=('Consolas', 10), state='disabled')
    console.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(console_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    console.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=console.yview)



    return winast