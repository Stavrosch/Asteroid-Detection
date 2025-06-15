import tkinter as tk
from tkinter import ttk
import asteroid_detection_window
import quick_eph_window
import platesolver_window
import customtkinter 
from PIL import Image, ImageTk


#-----To DO-----
# Custom Tkinter theme
def open_window_asteroid():
    asteroid_detection_window.create_window(root)

def open_window_quick_eph():
    quick_eph_window.create_window(root)


def open_platesolverwindow():
    platesolver_window.create_window(root)

  
root = customtkinter.CTk()
root.title("Main Window")
root.geometry("400x300")

label = customtkinter.CTkLabel(root, text="A.D.A", font=("fixedsys", 20))
label.place(x=270, y=40, anchor="n")

logo_photo = customtkinter.CTkImage(light_image=Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo_long.png'),
	dark_image=Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo_long.png'),size=(150, 300))
image_label = customtkinter.CTkLabel(root, image=logo_photo, text="")
image_label.place(x=0, y=0)


# CTkButton_asteroid = ttk.CTkButton(root, text="Track Asteroid", command=open_window_quick_eph)
# CTkButton_asteroid.place(relx=0.5, y=240, anchor="center")

CTkButton_quick = customtkinter.CTkButton(root, text="Quick Ephemeris", command=open_window_quick_eph)
CTkButton_quick.place(x=270, y=100, anchor="center")
CTkButton_plate = customtkinter.CTkButton(root, text="Plate Solve", command=open_platesolverwindow)
CTkButton_plate.place(x=270, y=140, anchor="center")

CTkButton_asteroid = customtkinter.CTkButton(root, text="Asteroid Detection", command=open_window_asteroid)
CTkButton_asteroid.place(x=270, y=180, anchor="center")

root.mainloop()
