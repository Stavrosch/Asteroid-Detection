import tkinter as tk
from tkinter import ttk
import asteroid_detection_window
import quick_eph_window
from PIL import Image, ImageTk
import platesolver_window

#import window2
#import window3
#import window4

###### TO DO ######
# 1. Make the GUI look better
# 2. Make the zero point calculation more faster by using a Catalogue
# 3. Make the apparent mag calc more accurate
# 4. Make the asteroid detection more accurate
# 5. Add explanations
# 6. Button to add option for calculation of residuals
def open_window_asteroid():
     asteroid_detection_window.create_window(root)
     
def open_window_quick_eph():
     quick_eph_window.create_window(root)

def open_platesolverwindow():
     platesolver_window.create_window(root)

# def open_window4():
#     window4.create_window(root)

root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")

label = tk.Label(root, text="A.D.A", font=("fixedsys", 20))
label.pack(pady=0)

logo = Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo.png').resize((120,120))
logo_photo = ImageTk.PhotoImage(logo)
image_label = tk.Label(root, image=logo_photo)
image_label.pack(pady=0)

button2 = ttk.Button(root, text="Quick Ephemeris", command=open_window_quick_eph)
button2.pack(pady=10)

button3 = ttk.Button(root, text="Plate Solve", command=open_platesolverwindow)
button3.pack(pady=10)

button1 = ttk.Button(root, text="Asteroid Detection", command=open_window_asteroid)
button1.pack(pady=10)

# button4 = ttk.Button(root, text="Option 4", command=open_window4)
# button4.pack(pady=10)

root.mainloop()