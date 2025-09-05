import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from astropy.io import fits
from astroquery.astrometry_net import AstrometryNet
import os
from Utilities import FOV_calc, residual_calc, ps_local ,solve_plate
from astropy.coordinates import Angle
import astropy.units as u
import requests
import subprocess


###### TO DO ######
# 1. Add a progress bar
# 2. Add if already solved, -> except if the checkbox is ticked
# 3. Add a button to open the solved image
# 4. Lock the button
# 5. Fix alignments
# 6. Add comm boxes that shows you which info will be used for plate solving.
# 7. Fix local solver with arguments

def choose_file(file_label, solve_button,result_label,progress_bar,ra_entry,dec_entry,scale_entry):
    global file_paths
    file_paths = filedialog.askopenfilenames(
        filetypes=[("FITS Files", "*.fits"), ("All Files", "*.*")],
        title="Select FITS files"
    )
    if file_paths:
        file_names = [os.path.basename(file_path) for file_path in file_paths]
        file_nums = len(file_names)
        file_path = file_paths[0]
        
        
        try:
            with fits.open(file_path) as file:
                hdu = file[0]
                header = hdu.header
                file.close()

            
                RA = header.get('RA')
                DEC = header.get('DEC')
                print(f"RA: {RA}, DEC: {DEC}")
                #pixscale = header.get('PIXSCALE') or header.get('PIXSIZE') or header.get('PIXSCL')
                #print(RA, DEC, pixscale)
            if RA is not None or DEC is not None:
                try:
                    RA = float(RA) 
                    DEC = float(DEC)
                except ValueError:
                    try:
                        RA = Angle(RA, unit=u.hourangle)
                        DEC =  Angle(DEC, unit=u.deg).degree
                        #print(f"Converted RA: {RA}, DEC: {DEC}")
                    except Exception as e:
                        #print(f"Error converting RA/DEC: {e}")
                        RA = "RA not found"
                        DEC = "Dec not found"
                #print(RA, DEC, pixscale)

                ra_entry.config(state='normal')
                ra_entry.delete(0, tk.END)
                ra_entry.insert(0, f"{RA:.2f}")
                
                dec_entry.config(state='normal')
                dec_entry.delete(0, tk.END)
                dec_entry.insert(0, f"{DEC:.2f}")
        except Exception as e:
            print(f"Error reading header: {e}")
            ra_entry.config(state='normal')
            ra_entry.delete(0, tk.END)
            ra_entry.insert(0, "-")
            
            dec_entry.config(state='normal')
            dec_entry.delete(0, tk.END)
            dec_entry.insert(0, "-")
    
        file_label.config(text=f"Selected {file_nums} Files.", fg="green")
        solve_button.config(state=tk.NORMAL)
        result_label.config(text=f" ")
        progress_bar['value'] = 0

    else:
        messagebox.showwarning("No Files Selected", "Please select valid FITS files.")
        file_label.config(text="No files selected", fg="red")
        solve_button.config(state=tk.DISABLED)
        

def choose_solver(root, file_label, result_label, result_fail_label, progress_bar,file_paths,var,var1):
    result_label.config(text="Starting plate solving...")
    result_fail_label.config(text="")
    if var1.get() == 1:
        ps_local(root, file_label, result_label, result_fail_label, progress_bar,var,file_paths)
    else:
        solve_plate(root, file_label, result_label, result_fail_label, progress_bar,var, file_paths)


def create_window(root):
    plate_solver_window = tk.Toplevel(root)
    plate_solver_window.title("Plate Solver")
    plate_solver_window.geometry("400x270")
    plate_solver_window.resizable(False, False)


    file_label = tk.Label(plate_solver_window, text="No files selected", fg="red")
    file_label.place(x=150, y=10)


    select_button = tk.Button(
        plate_solver_window,
        text="Choose Files",
        command=lambda: choose_file(file_label, solve_button, result_label, progress_bar,ra_entry,dec_entry,scale_entry)
    )
    select_button.place(x=50, y=8)
    
    var1 = tk.IntVar()
    solver_choice = tk.Checkbutton(
        plate_solver_window,
        text="Local?",
        variable=var1,
        onvalue=1,
        offvalue=0
    )
    solver_choice.place(x=50, y=50)
    
    ra_label = tk.Label(plate_solver_window, text="RA:")
    ra_label.place(x=150, y=50)
    ra_entry = tk.Entry(plate_solver_window, width=10, state="disabled")
    ra_entry.place(x=180, y=50)
    
    dec_label = tk.Label(plate_solver_window, text="Dec:")
    dec_label.place(x=150, y=80)
    dec_entry = tk.Entry(plate_solver_window, width=10, state="disabled")
    dec_entry.place(x=180, y=80)
    

    scale_label = tk.Label(plate_solver_window, text="Scale:")
    scale_label.place(x=270, y=80)
    scale_entry = tk.Entry(plate_solver_window, width=10, state="disabled")
    scale_entry.place(x=320, y=80)
    
    var = tk.IntVar()
    header_update = tk.Checkbutton(plate_solver_window,text="Make Copy?",variable=var,onvalue=1,offvalue=0)
    header_update.place(x=50, y=80)

    solve_button = tk.Button(
        plate_solver_window,
        text="Solve Plates",
        state=tk.DISABLED,
        command=lambda: choose_solver(
            root, file_label, result_label, result_fail_label,
            progress_bar, file_paths, var, var1
        )
    )
    solve_button.place(x=150, y=180, width=100)

    progress_bar = ttk.Progressbar(
        plate_solver_window,
        orient="horizontal",
        length=300,
        mode="determinate"
    )
    progress_bar.place(x=50, y=140)

    result_label = tk.Label(
        plate_solver_window,
        text="Results will appear here",
        wraplength=380
    )
    result_label.place(x=10, y=215)

    result_fail_label = tk.Label(plate_solver_window,text="",wraplength=380 )
    result_fail_label.place(x=10, y=240)

 

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("200x100")

    tk.Button(
        root,
        text="Open Plate Solver",
        command=lambda: create_window(root)
    ).pack(padx=20, pady=20)

    root.mainloop()