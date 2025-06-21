import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from astropy.io import fits
from Utilities import residual_calc_local
from astropy.coordinates import Angle
import astropy.units as u


def get_residual(file_path):
    corr_file = file_path.replace('.fits', '.corr')
    if os.path.exists(corr_file):
        residual = residual_calc_local.residual_calc_local(corr_file)
        if residual is not None:
            print(f"Residual RMS (arcsec): {residual:.4f}")
            return residual        

def ps_local(root, file_label, result_label, result_fail_label, progress_bar,var,file_paths):
    if not file_paths:
        result_label.config(text="No files selected.")
        return

    result_label.config(text="Starting local plate solving...")
    root.update_idletasks()

    progress_bar['maximum'] = len(file_paths)
    progress_bar['value'] = 0

    for i, file_path in enumerate(file_paths):
        try:
            print(var.get())
            if has_wcs(file_path) and var.get() == 0:
                result_label.config(text=f"Skipping {i+1}/{len(file_paths)}: Already solved.")
                root.update_idletasks()
                progress_bar['value'] += 1
                continue

            result_label.config(text=f"Solving {i+1}/{len(file_paths)}...")
            root.update_idletasks()
            try:
                with fits.open(file_path) as hdul:
                    header = hdul[0].header
                    ra = header.get('RA')
                    dec = header.get('DEC')
                    try:
                        ra_deg = float(ra)
                        dec_deg = float(dec)
                    except ValueError:
                        ra_deg = Angle(ra, unit=u.hourangle).degree
                        dec_deg = Angle(dec, unit=u.deg).degree
                        ra_deg = float(ra_deg)
                        dec_deg = float(dec_deg)
            except Exception as e:
                print(f"Error reading header: {e}")

            extra_args = []

            if ra_deg is not None and dec_deg is not None:
                extra_args += ['--ra', str(ra_deg), '--dec', str(dec_deg), '--radius', '2.0']

            cmd = [
                'wsl',
                'solve-field',
                '--overwrite',
                 '--new-fits', 'none',
                 '--solved', 'none',
                 #*extra_args,
                convert_path_to_wsl(file_path)
            ]
            
            # '--corr', 'none',
            #'--match', 'none',
            #'--rdls', 'none',
            print(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            wcs_file = file_path.replace('.fits', '.wcs')
            rdls_file = file_path.replace('.fits', '.rdls')
            if os.path.exists(wcs_file):
                with fits.open(wcs_file) as wcs_hdul:
                    wcs_header = wcs_hdul[0].header

                with fits.open(file_path, mode='update') as hdul:
                    current_header = hdul[0].header

                    current_header.remove("HISTORY", ignore_missing=True, remove_all=True)
                    current_header.remove("COMMENT", ignore_missing=True, remove_all=True)
                    current_header.update(wcs_header)
                    residual = get_residual(file_path)
                    current_header['COMMENT'] = f"Residuals: {residual} calculated by ADA."

                    hdul.flush()


                os.remove(wcs_file)
                result_label.config(text=f"Solved and updated {i+1}/{len(file_paths)}.")

            else:
                result_label.config(text=f"Solved {i+1}, but WCS file not found.")
            
            root.update_idletasks()

        except subprocess.CalledProcessError as e:
            result_fail_label.config(text=f"{i+1}/{len(file_paths)}: failed to solve.")
            print(f"Error solving {file_path}: {e}")
            root.update_idletasks()

        progress_bar['value'] += 1
        root.update_idletasks()

    result_label.config(text="Plate solving process completed for all files.")
    return
        
def convert_path_to_wsl(windows_path):
    """Convert C:\path\to\file to /mnt/c/path/to/file"""
    path = windows_path.replace('\\', '/')
    if path[1] == ':':
        return f"/mnt/{path[0].lower()}{path[2:]}"
    return path

def has_wcs(file_path):
    try:
        with fits.open(file_path) as hdul:
            header = hdul[0].header

            return 'CTYPE1' in header and 'CTYPE2' in header
    except Exception as e:
        print(f"Error checking WCS in {file_path}: {e}")
        return False
