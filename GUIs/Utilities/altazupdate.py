import tkinter as tk
from skyfield.api import load, Topos
from skyfield.data import mpc
import skyfield.units as u
import Utilities as ut

def update_live_altaz(designation_entry, lat_entry, lon_entry, height_entry, alt_var, az_var, ephemeris_window, asteroids_df, file_name):
    try:
        designation = designation_entry.get().strip()
        num = designation.zfill(5)
        result = ut.find_number_in_file(file_name, num)
        if result is None:
            alt_var.set("Not found")
            az_var.set("Not found")
            return

        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        height = float(height_entry.get())
        location = Topos(latitude_degrees=lat, longitude_degrees=lon, elevation_m=height)
        observer = earth + location
        now = ts.now()

        match = asteroids_df[asteroids_df['designation_packed'] == num]
        if match.empty:
            alt_var.set("No match")
            az_var.set("No match")
            return

        row = match.iloc[0]
        asteroid = sun + mpc.mpcorb_orbit(row, ts, GM_SUN)
        app = observer.at(now).observe(asteroid).apparent()
        alt, az, _ = app.altaz()

        alt_var.set(f"{alt.degrees:.2f}°")
        az_var.set(f"{az.degrees:.2f}°")
    except Exception as e:
        alt_var.set("Error")
        az_var.set("Error")

    ephemeris_window.after(5000, update_live_altaz)  # Refresh every 5 seconds