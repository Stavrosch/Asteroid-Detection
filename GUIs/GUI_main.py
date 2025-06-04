import tkinter as tk
from tkinter import ttk
import asteroid_detection_window
import quick_eph_window
import platesolver_window
from customtkinter import *
import track_asteroid
from PIL import Image, ImageTk


#-----To DO-----
# Custom Tkinter theme

def open_window_asteroid():
    asteroid_detection_window.create_window(root)
     
def open_window_quick_eph():
    quick_eph_window.create_window(root)

def open_platesolverwindow():
    platesolver_window.create_window(root)
    
def open_trackasteroid_window():
     track_asteroid.create_window(root)

root = tk.Tk()
root.title("Main Window")
root.geometry("400x340")

label = tk.Label(root, text="A.D.A", font=("fixedsys", 20))
label.place(relx=0.5, y=10, anchor="n")

logo = Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo.png') \
            .resize((120,120))
logo_photo = ImageTk.PhotoImage(logo)
image_label = tk.Label(root, image=logo_photo)
image_label.place(relx=0.5, y=50, anchor="n")


button_asteroid = ttk.Button(root, text="Track Asteroid", command=open_trackasteroid_window)
button_asteroid.place(relx=0.5, y=240, anchor="center")

button_quick = ttk.Button(root, text="Quick Ephemeris", command=open_window_quick_eph)
button_quick.place(relx=0.5, y=200, anchor="center")

button_plate = ttk.Button(root, text="Plate Solve", command=open_platesolverwindow)
button_plate.place(relx=0.5, y=280, anchor="center")

button_asteroid = ttk.Button(root, text="Asteroid Detection", command=open_window_asteroid)
button_asteroid.place(relx=0.5, y=320, anchor="center")

root.mainloop()
