import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests


def get_observable_objects(lat, lon, height,obs_time, angle=None, min_mag=None, max_mag=None, object_type=None, parent_frame=None):
        print(obs_time)
        
        params = {
            "optical": "true",
            "lat": lat,
            "lon": lon,
            "alt": height,
            "obs-time": obs_time.split("T")[0],
            "sb-kind": "a",
            "maxoutput": 100,
            "output-sort": "trans",
            "output-sort-r": "true",
            
        }
        
        if angle:
            params["elev-min"] = angle
        if min_mag:
            params["vmag-min"] = min_mag
        if max_mag:
            params["vmag-max"] = max_mag
        if object_type:
            params["sb-group"] = object_type
        print(params)
        response = requests.get("https://ssd-api.jpl.nasa.gov/sbwobs.api", params=params)

        if response.status_code != 200:
            messagebox.showerror("API Error", f"Failed to get data ({response.status_code})")
            return

        data = response.json()
        if "data" not in data:
            messagebox.showinfo("No Results", "No observable objects found.")
            return

        headers = data["fields"]
        rows = data["data"]
        fields_to_suppress = ["Object-Observer-Sun (deg)", "Topo.range (au)", "Galactic latitude (deg)", "Object-Observer-Moon (deg)", ""]
        suppress_indices = [headers.index(field) for field in fields_to_suppress if field in headers]
        filtered_headers = [header for i, header in enumerate(headers) if i not in suppress_indices]
        filtered_rows = [
            [value for j, value in enumerate(row) if j not in suppress_indices]
            for row in rows
        ]


        tree = ttk.Treeview(parent_frame, columns=filtered_headers, show="headings", height=10)
        for col in filtered_headers:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in filtered_rows:
            tree.insert("", "end", values=row)
        tree.place(x=220, y=10, width=800, height=300)