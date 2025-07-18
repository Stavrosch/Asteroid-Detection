import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from astropy.io import fits
from astroquery.astrometry_net import AstrometryNet
import os
from Utilities import FOV_calc, residual_calc
import requests
from astropy.coordinates import Angle
import astropy.units as u
from dotenv import load_dotenv
import os

def solve_plate(root, file_label, result_label, result_fail_label, progress_bar,var, file_paths):
    if not file_paths:
        result_label.config(text="No files selected.")
        return

    result_label.config(text="Starting plate solving...")
    root.update_idletasks()

    progress_bar['maximum'] = len(file_paths)
    progress_bar['value'] = 0
    load_dotenv()
    ASTROMETRY_API_KEY = os.getenv('API_KEY')
    print(f"Using Astrometry.net API key: {ASTROMETRY_API_KEY}")
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

                RA = header.get('RA')
                DEC = header.get('DEC')

                if RA is not None and DEC is not None:
                    try:
                        RA = float(RA) 
                        DEC = float(DEC)
                    except ValueError:
                        try:
                            RA = Angle(RA, unit=u.hourangle).degree
                            DEC =  Angle(DEC, unit=u.deg).degree

                        except Exception as e:
                            print(f"Error converting RA/DEC: {e}")
                    RA = float(RA)
                    DEC = float(DEC)
                    solve_kwargs = {'center_ra': RA, 'center_dec': DEC, 'radius': 5}
                else:
                    solve_kwargs = {}

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
                    if check==1:
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
    return
