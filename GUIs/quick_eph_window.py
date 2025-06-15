import tkinter as tk
from tkinter import ttk
from astroquery.mpc import MPC
from astropy.coordinates import EarthLocation
from datetime import datetime
import astropy.units as u
from astropy.coordinates import Angle
from astropy.time import Time
from pwi4_client import PWI4
import Utilities as ut
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, AltAz
import customtkinter
from skyfield.api import load, Topos
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.api import utc
import pandas as pd
import time
from skyfield.units import Angle
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from datetime import timedelta
import tkinter.font as tkFont  # Add at the top

# TO DO 
# LOAD TWILIGHT DATA

start = time.time()
asteroids_df = pd.read_pickle("GUIs/Utilities/mpcorb_df.pkl")
end = time.time()
print(f"Data loaded in {end - start:.2f} seconds")

file_name = "GUIs/Utilities/mpcorb_df.pkl"
eph = load('de421.bsp')
end2 = time.time()
print(f"Ephemeris loaded in {end2 - end:.2f} seconds")
sun, earth = eph['sun'], eph['earth']
ts = load.timescale()


def create_window(root):
    ephemeris_window = tk.Toplevel(root)
    ephemeris_window.title("Asteroid Tools")
    ephemeris_window.geometry("950x600")

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

    columns = ("RA", "Dec", "Mag", "Distance km", "au", "daily motion (deg)")
    ephem_table = ttk.Treeview(tab_ephemeris, columns=columns, show='headings', height=1)
    for col in columns:
        ephem_table.heading(col, text=col)
        ephem_table.column(col, width=90, anchor='center')
    ephem_table.place(x=10, y=10)

    graph_frame = tk.Frame(tab_ephemeris)
    graph_frame.place(x=265, y=80, width=650, height=350)
    fig, ax = plt.subplots(figsize=(7.5, 3), dpi=80)
    ax.set_xlabel("Time hours from now)")
    ax.set_ylim(0, 90)
    ax.set_xlim(0,10)
    ax.set_ylabel("Altitude (deg)")
    ax.set_title("Altitude Path")
    ax.grid(True)
    fig.tight_layout()


    
    duration_slider = tk.Scale(tab_ephemeris, from_=1, to=24, resolution=1, orient=tk.HORIZONTAL)
    duration_slider.place(x=540, y=320)
    duration_slider.set(10)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=0, y=0, width=620, height=240)
    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    toolbar.place(x=10, y=240)

    def refresh():
        for row in ephem_table.get_children():
            ephem_table.delete(row)

        
        designation = designation_entry.get().strip()
        number_to_find = designation
        num=number_to_find
        for i in range(5-len(number_to_find)):
            num='0'+num
        result=ut.find_number_in_file(file_name, num)
        if result is None:
            ephem_table.insert("", tk.END, values=[f"Not in MPCORB: {designation}"] + [""] * (len(columns) - 1))
            return

        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        height = float(height_entry.get())
        location = Topos(latitude_degrees=lat, longitude_degrees=lon, elevation_m=height)
        observer = earth + location
        dt = datetime.fromisoformat(time_entry.get()).replace(tzinfo=utc)
        duration_hr = duration_slider.get()
        start_time = ts.from_datetime(dt)
        end_time = ts.from_datetime(dt + timedelta(hours=duration_hr))
        times = ts.linspace(start_time, end_time, 100)
        now = ts.now()
        #print(asteroids_df.head())
        match = asteroids_df[asteroids_df['designation_packed'] == num]
        if match.empty:
            print(f"No match found for {num} in MPCORB")
            ephem_table.insert("", tk.END, values=[f"No match in MPCORB: {num}"] + ["-"] * (len(columns) - 1))
            return
        row = match.iloc[0]
        # print(f"Row data: {row}")
        # print(asteroids_df.columns)
        minor_planet = sun + mpc.mpcorb_orbit(row, ts, GM_SUN)
        orbit = mpc.mpcorb_orbit(row, ts, GM_SUN)

        alt_list, time_list = [], []
        astrometric = observer.at(times).observe(minor_planet)
        apparent = astrometric.apparent()
        alt, az, distance = apparent.altaz()
        alt_list = alt.degrees
        time_list = [(t - now) * 24 for t in times]

        t1=times[0]
        t1 = t1.utc_strftime('%Y-%m-%d %H:%M')
        ra_array, dec_array, _ = apparent.radec()
        ra_scalar = Angle(degrees=ra_array.degrees[0])
        dec_scalar = Angle(degrees=dec_array.degrees[0])
        print(type(ra_scalar), type(dec_scalar))
        ephem_table.insert("", tk.END, values=(
            ra_scalar.hstr(warn=False),
            dec_scalar.dstr(),
            f"{row['magnitude_H']:.2f}",
            f"{distance.km[0] / 1.496e+8:.3f} au",
            f"{row['semimajor_axis_au']:.3f}",
            f"{row['mean_daily_motion_degrees']:.2f}",
            "-"
        ))

        plot_asteroid_altaz_path(alt_list, time_list)



    def plot_asteroid_altaz_path(alt_list, time_list):
        above_list = []
        below_list = []
        break_points = []
        ax.clear()

        above = [(t, alt) for t, alt in zip(time_list, alt_list) if alt >= 0]
        below = [(t, alt) for t, alt in zip(time_list, alt_list) if alt < 0]
        if above:
            for segment in ut.split_segments(above):
                t_seg, alt_seg = zip(*segment)
                ax.plot(t_seg, alt_seg, 'r')
        if below:
            for segment in ut.split_segments(below):
                t_seg, alt_seg = zip(*segment)
                ax.plot(t_seg, alt_seg, 'grey')

        ax.set_xlabel("Time (hours from now)")
        ax.set_ylabel("Altitude (deg)")
        ax.set_title("Altitude Path")
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.6)
        ax.grid(True)
        ax.set_xlim(min(time_list), max(time_list))
        ax.set_ylim(min(0, min(alt_list) - 5), max(0, max(alt_list) + 5))
        canvas.draw()

    ttk.Button(tab_ephemeris, text="Refresh", command=refresh).place(x=650, y=10, width=50)

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

    ttk.Button(tab_orbital, text="Get Tracking Information", command=orbital_printer).place(x=10, y=10, width=140)
    ttk.Button(tab_orbital, text="Copy", command=copy_to_clipboard).place(x=150, y=10, width=60)

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


    ttk.Button(tab_neos, text="Get Observable Asteroids", command=get_neos).place(x=10, y=105, width=200)
    selected_listbox = tk.Listbox(tab_neos, height=10, width=50)
    selected_listbox.place(x=220, y=10)
    
    def on_listbox_select(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_name = event.widget.get(index)
            selected_name = selected_name.split(" ")[0] 
            designation_entry.delete(0, tk.END)
            designation_entry.insert(0, selected_name)

    selected_listbox.bind("<<ListboxSelect>>", on_listbox_select)

    tk.Label(tab_ephemeris,text="Altitude:").place(x=10, y=80)
    tk.Label(tab_ephemeris, text="Azimuth").place(x=10, y=100)
    
    telescope_comms = tk.Text(tab_ephemeris, wrap="word")
    telescope_comms.place(x=10, y=140, width=150, height=150)
    telescope_comms.insert("1.0", "Telescope Comms will apear here")

    def goto():
        print("Going to Asteroid")
        #pwi4 = PWI4()
        #if not pwi4.status().mount.is_connected:
            #pwi4.mount_connect()
        #pwi4.mount_radecpath_new()
        #for jd, ra, dec in points:
            #pwi4.mount_radecpath_add_point(jd, ra, dec)
        #pwi4.mount_radecpath_apply()
        
    ttk.Button(tab_ephemeris, text="GO TO", command=goto).place(x=180,y=80)

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
    root = customtkinter.CTk()
    root.title("Main Application")
    root.geometry("300x100")
    customtkinter.CTkButton(root, text="Open Ephemeris", command=lambda: create_window(root)).pack(padx=20, pady=20)
    root.mainloop()
