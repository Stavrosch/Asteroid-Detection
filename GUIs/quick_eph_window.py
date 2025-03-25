import tkinter as tk
from tkinter import ttk
from astroquery.mpc import MPC
from astropy.coordinates import EarthLocation
from datetime import datetime
import astropy.units as u
import subprocess
import Utilities as ut 


def create_window(root):
    ephemeris_window = tk.Toplevel(root)
    ephemeris_window.title("Asteroid Ephemeris")

    # Asteroid designation Button
    tk.Label(ephemeris_window, text="Asteroid Designation:").grid(row=0, column=0, padx=10, pady=5)
    designation_entry = tk.Entry(ephemeris_window)
    designation_entry.grid(row=0, column=1, padx=10, pady=5)
    designation_entry.insert(0, "1")  # Default asteroid designation

    # Location Selection
    tk.Label(ephemeris_window, text="Select Location:").grid(row=1, column=0, padx=10, pady=5)
    location_var = tk.StringVar()
    location_var.set("CYPRUS")
    location_combobox = ttk.Combobox(ephemeris_window, textvariable=location_var, values=["CYPRUS", "NOESIS", "HOLOMONTAS", "Custom"])
    location_combobox.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(ephemeris_window, text="Select Mount:").grid(row=2, column=0, padx=10, pady=5)
    mount_var = tk.StringVar()
    mount_var.set("PlaneWave4")
    mount_combobox = ttk.Combobox(ephemeris_window, textvariable=mount_var, values=["PlaneWave4", "10Micron"])
    mount_combobox.grid(row=2, column=1, padx=10, pady=5)

    def on_location_change(event):
        if location_var.get() == "Custom":
            open_custom_location_window()
        else:
            update_location_label()

    location_combobox.bind("<<ComboboxSelected>>", on_location_change)

    lat_label = tk.Label(ephemeris_window, text="Latitude: 34.932056")
    lat_label.grid(row=3, column=0, padx=10, pady=5)

    lon_label = tk.Label(ephemeris_window, text="Longitude: 32.840167")
    lon_label.grid(row=3, column=1, padx=10, pady=5)

    height_label = tk.Label(ephemeris_window, text="Height: 1411 m")
    height_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    tk.Label(ephemeris_window, text="Time (YYYY-MM-DDTHH:MM:SS):").grid(row=5, column=0, padx=10, pady=5)
    time_entry = tk.Entry(ephemeris_window)
    time_entry.grid(row=5, column=1, padx=10, pady=5)
    time_entry.insert(0, datetime.now().isoformat())  # Default to current time

    def set_time_now():
        time_entry.delete(0, tk.END)
        time_entry.insert(0, datetime.now().isoformat())

    tk.Button(ephemeris_window, text="Set to Now", command=set_time_now).grid(row=7, column=1, padx=10, pady=5)

    def get_ephemeris():
        asteroid_designation = designation_entry.get()
        
        if location_var.get() == "CYPRUS":
            location = EarthLocation(lat='34.932056', lon='32.840167', height=1411 * u.m)
        elif location_var.get() == "NOESIS":
            location = EarthLocation(lat='40.5624', lon='22.9956', height=68 * u.m)
        elif location_var.get() == "HOLOMONTAS":
            location = EarthLocation(lat='40.43291', lon='23.5055', height=800 * u.m)
        else:
            lat = float(custom_lat_entry.get())
            lon = float(custom_lon_entry.get())
            height = float(custom_height_entry.get()) * u.m
            location = EarthLocation(lat=lat, lon=lon, height=height)
        
        time = time_entry.get()
        if time.lower() == "now":
            time = datetime.now().isoformat()
        
        eph = MPC.get_ephemeris(asteroid_designation, location=location, start=time, number=1, 
                                ra_format={'sep': ':', 'unit': 'hourangle', 'precision': 3}, 
                                dec_format={'sep': ':', 'precision': 2})
        
        result_label.config(text=str(eph['Date', 'RA', 'Dec']))

    get_ephem_button = tk.Button(ephemeris_window, text="Get Ephemeris", command=get_ephemeris)
    get_ephem_button.grid(row=8, column=0, columnspan=2, pady=10)

    result_label = tk.Label(ephemeris_window, text="Ephemeris will appear here", wraplength=400)
    result_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def open_custom_location_window():
        custom_window = tk.Toplevel(ephemeris_window)
        custom_window.title("Custom Location Input")

        tk.Label(custom_window, text="Custom Latitude:").grid(row=0, column=0, padx=10, pady=5)
        global custom_lat_entry
        custom_lat_entry = tk.Entry(custom_window)
        custom_lat_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(custom_window, text="Custom Longitude:").grid(row=1, column=0, padx=10, pady=5)
        global custom_lon_entry
        custom_lon_entry = tk.Entry(custom_window)
        custom_lon_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(custom_window, text="Custom Height (m):").grid(row=2, column=0, padx=10, pady=5)
        global custom_height_entry
        custom_height_entry = tk.Entry(custom_window)
        custom_height_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(custom_window, text="Submit", command=lambda: [update_location_label(), custom_window.destroy()]).grid(row=3, column=0, columnspan=2, pady=10)

    def update_location_label():
        if location_var.get() == "CYPRUS":
            lat, lon, height = '34.932056', '32.840167', '1411 m'
        elif location_var.get() == "NOESIS":
            lat, lon, height = '40.5624', '22.9956', '68 m'
        elif location_var.get() == "HOLOMONTAS":
            lat, lon, height = '40.43291', '23.5055', '800 m'
        else:
            # Custom location
            lat = custom_lat_entry.get() or 'N/A'
            lon = custom_lon_entry.get() or 'N/A'
            height = custom_height_entry.get() or 'N/A'

        lat_label.config(text=f"Latitude: {lat}")
        lon_label.config(text=f"Longitude: {lon}")
        height_label.config(text=f"Height: {height}")
        
    
        # TLE Printer Button
    def tle_printer():
        asteroid_designation = designation_entry.get()
        mount = mount_var.get()

        tle = ut.TLE_printer(mount,asteroid_designation)
        tle_label.config(text=f"TLE: {tle}", font=("Helvetica", 8))

    tle_printer_button = tk.Button(ephemeris_window, text="TLE Printer", command=tle_printer)
    tle_printer_button.grid(row=10, column=0, columnspan=2, pady=10)
    tle_label = tk.Label(ephemeris_window, text="TLE will appear here", wraplength=400, font=("Helvetica", 8))
    tle_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    # Copy to Clipboard Button
    def copy_to_clipboard():
        tle_text = tle_label.cget("text")
        if tle_text and tle_text != "TLE will appear here":
            ephemeris_window.clipboard_clear()
            tle_text1 = tle_text[len("TLE: Line found:"):]
            ephemeris_window.clipboard_append(tle_text1)
            ephemeris_window.update()
            

    copy_button = tk.Button(ephemeris_window, text="Copy", command=copy_to_clipboard)
    copy_button.grid(row=12, column=1, padx=10, pady=5)