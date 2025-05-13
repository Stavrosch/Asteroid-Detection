import tkinter as tk
from tkinter import ttk
from astroquery.mpc import MPC
from astropy.coordinates import EarthLocation
from datetime import datetime
import astropy.units as u
import Utilities as ut

def create_window(root):
    ephemeris_window = tk.Toplevel(root)
    ephemeris_window.title("Asteroid Ephemeris")
    ephemeris_window.geometry("450x400")

    # Asteroid designation
    tk.Label(ephemeris_window, text="Asteroid Designation:") \
        .place(x=10, y=10)
    designation_entry = tk.Entry(ephemeris_window)
    designation_entry.place(x=130, y=10, width=50)
    designation_entry.insert(0, "1")  

    # Location selection
    tk.Label(ephemeris_window, text="Select Location:") \
        .place(x=10, y=40)
    location_var = tk.StringVar(value="AUTH-3")
    location_combobox = ttk.Combobox(
        ephemeris_window,
        textvariable=location_var,
        values=["AUTH-3", "AUTH-1", "AUTH-2", "Custom"],
        state="readonly"
    )
    location_combobox.place(x=100, y=40, width=80)
    location_combobox.bind("<<ComboboxSelected>>", lambda e: on_location_change())

    # Mount selection
    tk.Label(ephemeris_window, text="Select Mount:") \
        .place(x=190, y=40)
    mount_var = tk.StringVar(value="PlaneWave4")
    mount_combobox = ttk.Combobox(
        ephemeris_window,
        textvariable=mount_var,
        values=["PlaneWave4", "10Micron"],
        state="readonly"
    )
    mount_combobox.place(x=270, y=40, width=100)

    # Latitude / Longitude / Height display
    lat_label = tk.Label(ephemeris_window, text="Latitude:")
    lat_label.place(x=10, y=70)
    lat_entry = tk.Entry(ephemeris_window)
    lat_entry.place(x=65, y=70, width=70)
    lat_entry.insert(0, 34.932056)
    
    lon_label = tk.Label(ephemeris_window, text="Longitude: ")
    lon_label.place(x=140, y=70)
    lon_entry = tk.Entry(ephemeris_window)
    lon_entry.place(x=205, y=70, width=70)
    lon_entry.insert(0, 32.840167)
    height_label = tk.Label(ephemeris_window, text="Height:")
    height_label.place(x=280, y=70)
    height_entry = tk.Entry(ephemeris_window)
    height_entry.place(x=330, y=70, width=40)
    height_entry.insert(0, 1411)

    # Time entry
    tk.Label(ephemeris_window, text="Time:") \
        .place(x=10, y=100)
    time_entry = tk.Entry(ephemeris_window)
    time_entry.place(x=50, y=102, width=170)
    time_entry.insert(0, datetime.now().isoformat())
    
    tk.Button(
        ephemeris_window,
        text="Set to Now",
        command=lambda: time_entry.delete(0, tk.END) or time_entry.insert(0, datetime.now().isoformat())
    ).place(x=235, y=97, width=80)



    # Get Ephemeris button
    def get_ephemeris():
        asteroid_designation = designation_entry.get()

        lat = lat_entry.get()
        lon = lon_entry.get()
        height = height_entry.get()
        location = EarthLocation(lat=float(lat)*u.deg, lon=float(lon)*u.deg, height=float(height)*u.m)
        t = time_entry.get()
        if t.lower() == "now":
            t = datetime.now().isoformat()

        eph = MPC.get_ephemeris(
            asteroid_designation,
            location=location,
            start=t,
            number=1,
            ra_format={'sep': ':', 'unit': 'hourangle', 'precision': 3},
            dec_format={'sep': ':', 'precision': 2}
        )
        if len(eph) == 0:
            result_label.config(text="No ephemeris data returned")
            return

        row = eph[0]   # ← Astropy Table indexing instead of .iloc
        formatted = (
            f"Date:  {row['Date']}\n"
            f"RA  :  {row['RA']}\n"
            f"Dec :  {row['Dec']}"
        )
        result_label.config(text=formatted)

    separator = ttk.Separator(ephemeris_window, orient='horizontal')
    separator.place(relx=0, y=130, relwidth=10, relheight=1)
        
    tk.Button(
        ephemeris_window,
        text="Get Ephemeris",
        command=get_ephemeris
    ).place(x=10, y=140, width=120)        
            
            # Result label
    result_label = tk.Label(
        ephemeris_window,
        text="Ephemeris will appear here",
        wraplength=400,
        justify="left"
    )
    result_label.place(x=10, y=180)

    def orbital_printer():
        asteroid_designation = designation_entry.get()
        full_orb = ut.ORB_EL_printer(mount_var.get(), asteroid_designation)

        short = full_orb[:40]
        print(short)
        orbital_elements.delete(0, tk.END)
        orbital_elements.insert(0, full_orb)




    tk.Button(
        ephemeris_window,
        text="Orbital Elements",
        command=orbital_printer
    ).place(x=220, y=140, width=100)


    tle_label = tk.Label(
        ephemeris_window,
        text="Orbital Elements will appear here",
        wraplength=400,
        font=("Helvetica", 8),
        justify="left"
    )
    tle_label.place(x=210, y=180)
    
    
    orbital_elements = tk.Entry(ephemeris_window)
    orbital_elements.place(x=210, y=180, width=200)
    orbital_elements.insert(0, "Orbital Elements will appear here")
    #orbital_elements.config(state="readonly")
    


    def copy_to_clipboard():
        orb_text = orbital_elements.get()
        if orb_text:
            ephemeris_window.clipboard_clear()
            ephemeris_window.clipboard_append(orb_text.split(":", 1)[1].strip())
            ephemeris_window.update()

    tk.Button(
        ephemeris_window,
        text="Copy",
        command=copy_to_clipboard
    ).place(x=350, y=140, width=50)
    
    def get_neos():
        # determine lat, lon, height for API
        loc = location_var.get()
        latv = lat_entry.get()
        lonv = lon_entry.get()
        hv = height_entry.get()
        obs_time = time_entry.get()
        ut.get_observable_objects(latv, lonv, hv, obs_time)

    tk.Button(
        ephemeris_window,
        text="Get Observable NEOs",
        command=get_neos
    ).place(x=150, y=390, width=200)

    # Custom location window logic
    def on_location_change():
        if location_var.get() == "Custom":
            lat_entry.delete(0, tk.END)
            lon_entry.delete(0, tk.END)
            height_entry.delete(0, tk.END)
        else:
            update_location_label()

    def update_location_label():
        loc = location_var.get()
        if loc == "AUTH-3":
            lat, lon, h = '34.932056', '32.840167', '1411'
        elif loc == "AUTH-1":
            lat, lon, h = '40.5624', '22.9956', '68'
        elif loc == "AUTH-2":
            lat, lon, h = '40.43291', '23.5055', '800'
        else:
            lat_entry.delete(0, tk.END)
            lon_entry.delete(0, tk.END)
            height_entry.delete(0, tk.END)
        lat_entry.delete(0, tk.END)
        lat_entry.insert(0, lat)
        lon_entry.delete(0, tk.END)
        lon_entry.insert(0, lon)
        height_entry.delete(0, tk.END)
        height_entry.insert(0, h)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("300x100")
    tk.Button(
        root,
        text="Open Ephemeris",
        command=lambda: create_window(root)
    ).pack(padx=20, pady=20)
    root.mainloop()
