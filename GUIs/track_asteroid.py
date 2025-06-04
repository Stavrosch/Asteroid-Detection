import tkinter as tk
from tkinter import ttk
from astroquery.mpc import MPC
from astropy.coordinates import EarthLocation, Angle
from astropy.time import Time
import astropy.units as u
from pwi4_client import PWI4

def create_window(parent):
    win = tk.Toplevel(parent)
    win.title("Asteroid Tracking")
    win.geometry("400x400")

    tk.Label(win, text="Asteroid Designation:").pack()
    designation_entry = tk.Entry(win)
    designation_entry.pack()
    designation_entry.insert(0, "433")  # default Eros

    tk.Label(win, text="Start Time (UTC):").pack()
    start_entry = tk.Entry(win)
    start_entry.pack()
    start_entry.insert(0, Time.now().isot)

    tk.Label(win, text="Number of Points:").pack()
    npts_entry = tk.Entry(win)
    npts_entry.pack()
    npts_entry.insert(0, "10")

    tk.Label(win, text="Interval (minutes):").pack()
    interval_entry = tk.Entry(win)
    interval_entry.pack()
    interval_entry.insert(0, "1")

    tk.Label(win, text="Lat/Lon/Height:").pack()
    lat_entry = tk.Entry(win); lat_entry.pack(); lat_entry.insert(0, "34.93")
    lon_entry = tk.Entry(win); lon_entry.pack(); lon_entry.insert(0, "32.84")
    h_entry = tk.Entry(win); h_entry.pack(); h_entry.insert(0, "1411")

    result_label = tk.Label(win, text="")
    result_label.pack()

    def upload_path():
        designation = designation_entry.get()
        start_time = start_entry.get()
        num_points = int(npts_entry.get())
        interval_min = int(interval_entry.get())
        location = EarthLocation(
            lat=float(lat_entry.get())*u.deg,
            lon=float(lon_entry.get())*u.deg,
            height=float(h_entry.get())*u.m,
        )

        eph = MPC.get_ephemeris(
            designation,
            location=location,
            start=start_time,
            number=num_points,
            step=f"{interval_min}m"
        )

        points = []
        for row in eph:
            jd = Time(row['Date']).jd
            ra = Angle(row['RA'], unit=u.hourangle).hour
            dec = Angle(row['Dec'], unit=u.deg).degree
            points.append((jd, ra, dec))

        pwi4 = PWI4()
        if not pwi4.status().mount.is_connected:
            pwi4.mount_connect()
        pwi4.mount_radecpath_new()
        for jd, ra, dec in points:
            pwi4.mount_radecpath_add_point(jd, ra, dec)
        pwi4.mount_radecpath_apply()
        result_label.config(text="Asteroid tracking path uploaded!")

    tk.Button(win, text="Upload Tracking Path", command=upload_path).pack(pady=10)

# Test window alone:
if __name__ == "__main__":
    root = tk.Tk()
    create_window(root)
    root.mainloop()
