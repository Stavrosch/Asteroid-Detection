import tkinter as tk
from tkinter import ttk
import asteroid_detection_window
import quick_eph_window
#import window2
#import window3
#import window4

def open_window_asteroid():
     asteroid_detection_window.create_window(root)
     
def open_window_quick_eph():
     quick_eph_window.create_window(root)

# def open_window3():
#     window3.create_window(root)

# def open_window4():
#     window4.create_window(root)

root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")

label = tk.Label(root, text="ADAUTH", font=("Helvetica", 25))
label.pack(pady=20)

button1 = ttk.Button(root, text="Asteroid Detection", command=open_window_asteroid)
button1.pack(pady=10)

button2 = ttk.Button(root, text="Quick Ephemeris", command=open_window_quick_eph)
button2.pack(pady=10)

button3 = ttk.Button(root, text="Plate Solve")#, command=open_window3)
button3.pack(pady=10)

# button4 = ttk.Button(root, text="Option 4", command=open_window4)
# button4.pack(pady=10)

root.mainloop()