import tkinter as tk
from tkinter import ttk
from astroquery.mpc import MPC
from astropy.coordinates import EarthLocation
from datetime import datetime
import astropy.units as u
import Utilities as ut

def create_window(root):
    ephemeris_window = tk.Toplevel(root)
    ephemeris_window.title("Asteroid Tools")
    ephemeris_window.geometry("500x350")


    notebook = ttk.Notebook(ephemeris_window)
    notebook.place(x=0, y=145, relwidth=1, relheight=1)

    tab_ephemeris = tk.Frame(notebook)
    tab_orbital = tk.Frame(notebook)
    tab_neos = tk.Frame(notebook)

    notebook.add(tab_ephemeris, text='Ephemeris')
    notebook.add(tab_orbital, text='Orbital Elements')
    notebook.add(tab_neos, text='Whats Observable?')
    
    designation_entry = tk.Entry(ephemeris_window)
    designation_entry.place(x=130, y=10, width=50)
    designation_entry.insert(0, "1")
    tk.Label(ephemeris_window, text="Asteroid Designation:").place(x=10, y=10)

    location_var = tk.StringVar(value="AUTH-3")
    location_combobox = ttk.Combobox(ephemeris_window, textvariable=location_var, values=["AUTH-3", "AUTH-1", "AUTH-2", "Custom"], state="readonly")
    location_combobox.place(x=100, y=40, width=80)
    tk.Label(ephemeris_window, text="Select Location:").place(x=10, y=40)

    mount_var = tk.StringVar(value="PlaneWave4")
    mount_combobox = ttk.Combobox(ephemeris_window, textvariable=mount_var, values=["PlaneWave4", "10Micron"], state="readonly")
    mount_combobox.place(x=270, y=40, width=100)
    tk.Label(ephemeris_window, text="Select Mount:").place(x=190, y=40)

    lat_entry = tk.Entry(ephemeris_window)
    lat_entry.place(x=65, y=70, width=70)
    lat_entry.insert(0, 34.932056)
    tk.Label(ephemeris_window, text="Latitude:").place(x=10, y=70)

    lon_entry = tk.Entry(ephemeris_window)
    lon_entry.place(x=205, y=70, width=70)
    lon_entry.insert(0, 32.840167)
    tk.Label(ephemeris_window, text="Longitude: ").place(x=140, y=70)

    height_entry = tk.Entry(ephemeris_window)
    height_entry.place(x=330, y=70, width=40)
    height_entry.insert(0, 1411)
    tk.Label(ephemeris_window, text="Height:").place(x=280, y=70)

    time_entry = tk.Entry(ephemeris_window)
    time_entry.place(x=50, y=102, width=170)
    time_entry.insert(0, datetime.now().isoformat())
    tk.Label(ephemeris_window, text="Time:").place(x=10, y=100)

    tk.Button(ephemeris_window, text="Set to Now", command=lambda: time_entry.delete(0, tk.END) or time_entry.insert(0, datetime.now().isoformat())).place(x=235, y=97, width=80)

    result_label = tk.Label(tab_ephemeris, text="Ephemeris will appear here", wraplength=400, justify="left")
    result_label.place(x=10, y=50)

    def get_ephemeris():
        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        height = float(height_entry.get())
        location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=height*u.m)
        t = time_entry.get() if time_entry.get().lower() != "now" else datetime.now().isoformat()
        eph = MPC.get_ephemeris(designation_entry.get(), location=location, start=t, number=1,
                                ra_format={'sep': ':', 'unit': 'hourangle', 'precision': 3},
                                dec_format={'sep': ':', 'precision': 2})
        if len(eph) == 0:
            result_label.config(text="No ephemeris data returned")
            return
        row = eph[0]
        result_label.config(text=f"Date:  {row['Date']}\nRA  :  {row['RA']}\nDec :  {row['Dec']}")

    tk.Button(tab_ephemeris, text="Get Ephemeris", command=get_ephemeris).place(x=10, y=10, width=120)

    orbital_elements = tk.Text(tab_orbital, wrap="word")
    orbital_elements.place(x=10, y=60, width=460, height=90)
    orbital_elements.insert("1.0", "Orbital Elements will appear here")


    def orbital_printer():
        orb = ut.ORB_EL_printer(mount_var.get(), designation_entry.get())
        orbital_elements.delete("1.0", tk.END)
        orbital_elements.insert("1.0", orb)

    def copy_to_clipboard():
        orb_text = orbital_elements.get("1.0", tk.END).strip()
        if orb_text:
                ephemeris_window.clipboard_clear()
                ephemeris_window.clipboard_append(orb_text.split(":", 1)[-1].strip())
                ephemeris_window.update()

    tk.Button(tab_orbital, text="Get Tracking Information", command=orbital_printer).place(x=10, y=10, width=140)
    tk.Button(tab_orbital, text="Copy", command=copy_to_clipboard).place(x=150, y=10, width=60)

    def get_neos():
        lat = lat_entry.get()
        lon = lon_entry.get()
        height = height_entry.get()
        obs_time = time_entry.get()
        angle = None
        min_mag = None
        max_mag = None
        object_type = None
        
        if angle_entry.get() != '':
            angle = float(angle_entry.get())
        if min_mag_entry.get() != '':
            min_mag = float(min_mag_entry.get())
        if max_mag_entry.get() != '':  
            max_mag = float(max_mag_entry.get())
        if object_type_var.get() != "all objects":
            object_type = object_type_var.get()
        
        ut.get_observable_objects(lat, lon, height, obs_time, angle, min_mag, max_mag, object_type,
                                on_select_callback=add_selected_to_list)
    def add_selected_to_list(selected_data,filtered_headers):
        selected_listbox.delete(0, tk.END)  
        name_idx = filtered_headers.index("Name") if "Name" in filtered_headers else 0 
        for row in selected_data:
                selected_listbox.insert(tk.END, row[name_idx])
            
            
    angle_entry = tk.Entry(tab_neos)
    angle_entry.place(x=105, y=10, width=30)
    tk.Label(tab_neos, text="Elevation(deg) :").place(x=10, y=10)
    angle_entry.insert(0, "30")
    angle_entry.config(state="normal")

    
    tk.Label(tab_neos, text="V Mag:").place(x=10, y=40)
    min_mag_entry = tk.Entry(tab_neos)
    min_mag_entry.place(x=70, y=40, width=30)
    min_mag_entry.insert(0, "14")

    tk.Label(tab_neos, text="-").place(x=105, y=40)
    max_mag_entry = tk.Entry(tab_neos)
    max_mag_entry.place(x=120, y=40, width=30)
    max_mag_entry.insert(0, "18")
    
    tk.Label(tab_neos, text="Object Type:").place(x=10, y=70)
    object_type_var = tk.StringVar(value="NEO")
    object_type_menu = ttk.Combobox(
        tab_neos, textvariable=object_type_var,
        values=["all objects", "PHA", "NEO"], state="readonly"
    )
    object_type_menu.place(x=100, y=70, width=100)


    tk.Button(tab_neos, text="Get Observable Asteroids", command=get_neos).place(x=10, y=105, width=200)
    selected_listbox = tk.Listbox(tab_neos, height=10, width=50)
    selected_listbox.place(x=220, y=10)

    def on_location_change():
        if location_var.get() == "Custom":
            lat_entry.delete(0, tk.END)
            lon_entry.delete(0, tk.END)
            height_entry.delete(0, tk.END)
        else:
            update_location_label()

    def update_location_label():
        locations = {
            "AUTH-3": ('34.932056', '32.840167', '1411'),
            "AUTH-1": ('40.5624', '22.9956', '68'),
            "AUTH-2": ('40.43291', '23.5055', '800')
        }
        lat, lon, h = locations.get(location_var.get(), ('', '', ''))
        lat_entry.delete(0, tk.END)
        lat_entry.insert(0, lat)
        lon_entry.delete(0, tk.END)
        lon_entry.insert(0, lon)
        height_entry.delete(0, tk.END)
        height_entry.insert(0, h)

    location_combobox.bind("<<ComboboxSelected>>", lambda e: on_location_change())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("300x100")
    tk.Button(root, text="Open Ephemeris", command=lambda: create_window(root)).pack(padx=20, pady=20)
    root.mainloop()
