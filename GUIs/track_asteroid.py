import tkinter as tk
from tkinter import ttk
from pwi4_client import PWI4
from datetime import datetime
import time

class TelescopeControl:
    def __init__(self, pwi_client):
        self.pwi = pwi_client

    def connect_mount(self):
        status = self.pwi.mount_connect()
        return status.mount.is_connected

    def slew_to_ra_dec(self, ra_hours, dec_degs):
        self.pwi.mount_goto_ra_dec_j2000(ra_hours, dec_degs)

    def get_status(self):
        return self.pwi.status()

def create_enhanced_gui(root):
    pwi_client = PWI4()
    telescope = TelescopeControl(pwi_client)

    window = tk.Toplevel(root)
    window.title("Enhanced Asteroid Control")
    window.geometry("600x500")

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill='both')

    status_tab = ttk.Frame(notebook)
    control_tab = ttk.Frame(notebook)

    notebook.add(status_tab, text="Real-time Status")
    notebook.add(control_tab, text="Direct Telescope Control")

    # Status Tab Widgets
    status_label = tk.Label(status_tab, text="Mount Status:", font=("Arial", 12))
    status_label.pack(pady=10)

    status_text = tk.Text(status_tab, width=70, height=20, state='disabled')
    status_text.pack()

    def update_status():
        status = telescope.get_status()
        status_text.config(state='normal')
        status_text.delete(1.0, tk.END)
        status_text.insert(tk.END, f"RA: {status.mount.ra_j2000_hours:.4f} hours\n")
        status_text.insert(tk.END, f"Dec: {status.mount.dec_j2000_degs:.4f} deg\n")
        status_text.insert(tk.END, f"Alt: {status.mount.altitude_degs:.2f} deg\n")
        status_text.insert(tk.END, f"Az: {status.mount.azimuth_degs:.2f} deg\n")
        status_text.insert(tk.END, f"Slewing: {'Yes' if status.mount.is_slewing else 'No'}\n")
        status_text.config(state='disabled')
        window.after(2000, update_status)

    update_status()

    # Control Tab Widgets
    tk.Label(control_tab, text="RA (hours):").pack(pady=5)
    ra_entry = tk.Entry(control_tab)
    ra_entry.pack(pady=5)

    tk.Label(control_tab, text="Dec (degrees):").pack(pady=5)
    dec_entry = tk.Entry(control_tab)
    dec_entry.pack(pady=5)

    def connect_and_slew():
        connected = telescope.connect_mount()
        if connected:
            ra = float(ra_entry.get())
            dec = float(dec_entry.get())
            telescope.slew_to_ra_dec(ra, dec)
            result_label.config(text="Slew command sent!")
        else:
            result_label.config(text="Failed to connect mount!")

    tk.Button(control_tab, text="Connect & Slew", command=connect_and_slew).pack(pady=10)
    result_label = tk.Label(control_tab, text="")
    result_label.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("300x100")
    tk.Button(root, text="Open Enhanced Asteroid GUI", command=lambda: create_enhanced_gui(root)).pack(padx=20, pady=20)
    root.mainloop()
