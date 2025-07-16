import tkinter as tk
from PIL import Image, ImageTk
import asteroid_detection_window
import quick_eph_window
import platesolver_window
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, 'logowithouttext.png')
long_logo_path = os.path.join(BASE_DIR, 'logo_long.png')
background_path = os.path.join(BASE_DIR, 'bkgr-1.png') 


def open_window_asteroid():
    asteroid_detection_window.create_window(basikoparathiro)
    
def open_window_quick_eph():
    quick_eph_window.create_window(basikoparathiro)
    
def open_platesolverwindow():
    platesolver_window.create_window(basikoparathiro)

basikoparathiro = tk.Tk()
basikoparathiro.title("Asteroid Detector")
basikoparathiro.geometry("450x350")


bg_image = Image.open(background_path)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(basikoparathiro, image=bg_photo)
background_label.image = bg_photo  
background_label.place(x=0, y=0, relwidth=1, relheight=1)


logo2 = Image.open(logo_path) #.resize((144, 108))
logo_photo2 = ImageTk.PhotoImage(logo2)
basikoparathiro.iconphoto(False, logo_photo2)

titlos = tk.Label(basikoparathiro, text="Asteroid Detector", font=("fixedsys", 18))
titlos.place(relx=0.5, rely=0.13, anchor="n")

long_logo = Image.open(logo_path).resize((75, 75))
logoauth = ImageTk.PhotoImage(long_logo)
authlog = tk.Label(basikoparathiro, image=logoauth)
authlog.image = logoauth 
authlog.place(relx=0.91, rely=0.91, anchor="s")

button1 = tk.Button(basikoparathiro, text="Track Asteroid", command=open_window_quick_eph, 
                bg="#4f1ed6", fg="white", font=("fixedsys", 12), relief=tk.FLAT, borderwidth=3)
button1.place(relx=0.5, rely=0.35, anchor="center", width=150, height=30)

button2 = tk.Button(basikoparathiro, text="Plate Solve", command=open_platesolverwindow, 
                bg="#4f1ed6", fg="white", font=("fixedsys", 12), relief=tk.FLAT, borderwidth=3)
button2.place(relx=0.5, rely=0.50, anchor="center", width=150, height=30)

button3 = tk.Button(basikoparathiro, text="Asteroid Detection", command=open_window_asteroid, 
                bg="#4f1ed6", fg="white", font=("fixedsys", 12), relief=tk.FLAT, borderwidth=3)
button3.place(relx=0.5, rely=0.65, anchor="center", width=150, height=30)

basikoparathiro.mainloop()