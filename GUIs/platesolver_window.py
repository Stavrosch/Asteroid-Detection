import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from astropy.io import fits
from astroquery.astrometry_net import AstrometryNet
import os
from Utilities import FOV_calc, residual_calc
import requests

###### TO DO ######
# 1. Add a progress bar
# 2. Add if already solved, skip
# 3. Add a button to open the solved image
# 4. Lock the button
# 5. Fix alignments

def choose_file(file_label, solve_button,result_label,progress_bar):
    global file_paths
    file_paths = filedialog.askopenfilenames(
        filetypes=[("FITS Files", "*.fits"), ("All Files", "*.*")],
        title="Select FITS files"
    )
    if file_paths:
        file_names = [os.path.basename(file_path) for file_path in file_paths]
        file_nums = len(file_names)
        file_label.config(text=f"Selected {file_nums} Files.", fg="green")
        solve_button.config(state=tk.NORMAL)
        result_label.config(text=f" ")
        progress_bar['value'] = 0

    else:
        messagebox.showwarning("No Files Selected", "Please select valid FITS files.")
        file_label.config(text="No files selected", fg="red")
        solve_button.config(state=tk.DISABLED)

def solve_plate(root, file_label, result_label, result_fail_label, progress_bar,var):
    if not file_paths:
        result_label.config(text="No files selected.")
        return

    result_label.config(text="Starting plate solving...")
    root.update_idletasks()

    progress_bar['maximum'] = len(file_paths)
    progress_bar['value'] = 0
    ASTROMETRY_API_KEY = 'rdukoneutpiciaaa'
    ast = AstrometryNet()
    ast.api_key = ASTROMETRY_API_KEY
    for i, file_path in enumerate(file_paths):
        try:
            with fits.open(file_path) as file:
                hdu = file[0]
                header = hdu.header
                wcs = hdu.header
                print('\n',file_path)
                file.close()

                # # Check if the file already has a WCS header
                # if 'WCSAXES' in header:
                #     result_label.config(text=f"Skipping {i+1}/{len(file_paths)}: Already solved.")
                #     root.update_idletasks()
                #     progress_bar['value'] += 1

                #     continue

                RA = header.get('RA', '0')
                DEC = header.get('DEC', '0')

                RA = float(RA)
                DEC = float(DEC)

                solve_kwargs = {
                    'center_ra': RA,
                    'center_dec': DEC,
                    'radius': 5,  # degrees
                }

                result_label.config(text=f"Submitting {i+1}/{len(file_paths)} to Astrometry.net...")
                root.update_idletasks()

                wcs_header,subid = ast.solve_from_image(file_path,
                     force_image_upload=True,
                     publicly_visible='n',
                     solve_timeout=300,
                     return_submission_id=True,
                     **solve_kwargs
                )

                
                if wcs_header is not None:
                    result_label.config(text=f"Plate solving successful for image {i+1}/{len(file_paths)}!")
                    root.update_idletasks()
                    check = var.get()
                    #print(wcs_header)
                    if check==0:
                        with fits.open(file_path, mode='update') as hdul:
                                current_header = hdul[0].header
                                 # Safely remove all HISTORY/COMMENT entries (even if none exist)
                                current_header.remove("HISTORY", ignore_missing=True, remove_all=True)
                                current_header.remove("COMMENT", ignore_missing=True, remove_all=True)

                                current_header.update(wcs_header)
                                hdul.flush()
                                file.close()
                        with fits.open(file_path, mode='update') as hdul:
                            
                            header = hdul[0].header                           
                            print(subid)
                            status_url = f"http://nova.astrometry.net/api/submissions/{subid}"
                            response = requests.get(status_url)
                            data = response.json()
                            jobid = data.get("jobs", [])
                            print(jobid[0])
                            residuals = residual_calc(hdu,jobid[0])
                            #print(residuals)
                            header['COMMENT'] = f"Residuals: {residuals} calculated by ADA."
                            hdul.flush()


                    result_label.config(text=f"Plate solving complete for image {i+1}/{len(file_paths)}.")
                    root.update_idletasks()

        except Exception as e:
            result_fail_label.config(text=f"{i+1}/{len(file_paths)}: failed to solve.")
            print(e)
            root.update_idletasks()

        progress_bar['value'] += 1
        root.update_idletasks()

    result_label.config(text="Plate solving process completed for all files.")

def create_window(root):
    plate_solver_window = tk.Toplevel(root)
    plate_solver_window.title("Plate Solver")
    plate_solver_window.geometry("400x250")

    # File selection
    tk.Label(plate_solver_window, text="FITS File Path:").grid(row=0, column=0, padx=10, pady=5)
    file_label = tk.Label(plate_solver_window, text="No files selected", fg="red")
    file_label.grid(row=0, column=1, padx=10, pady=5)
    select_button = tk.Button(plate_solver_window, text="Select Files", command=lambda: choose_file(file_label, solve_button,result_label,progress_bar))
    select_button.grid(row=0, column=2, padx=10, pady=5)

    # Solve button
    solve_button = tk.Button(plate_solver_window, text="Solve Plates", state=tk.DISABLED, command=lambda: solve_plate(root, file_label, result_label, result_fail_label, progress_bar,var))
    solve_button.grid(row=1, column=0, columnspan=3, pady=10)

    # Progress bar
    progress_bar = ttk.Progressbar(plate_solver_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Result display
    result_label = tk.Label(plate_solver_window, text="Results will appear here", wraplength=400)
    result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    result_fail_label = tk.Label(plate_solver_window, text="", wraplength=400)
    result_fail_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    var = tk.IntVar()
    header_update = tk.Checkbutton(plate_solver_window, text=f'Dont Update Header?',variable=var, onvalue=1, offvalue=0)# command=print_selection)
    header_update.grid(row=4, column=3, columnspan=3, padx=10, pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")

    tk.Button(root, text="Open Plate Solver", command=lambda: create_window(root)).pack(padx=20, pady=20)

    root.mainloop()