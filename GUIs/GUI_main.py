import tkinter as tk
from tkinter import ttk
import asteroid_detection_window
import quick_eph_window
import platesolver_window
import customtkinter 
from PIL import Image, ImageTk

def open_window_asteroid():
    asteroid_detection_window.create_window(basikoparathiro)
def open_window_quick_eph():
    quick_eph_window.create_window(basikoparathiro)
def open_platesolverwindow():
    platesolver_window.create_window(basikoparathiro)
basikoparathiro=customtkinter.CTk()
basikoparathiro.title("Asteroid Detector")
basikoparathiro.geometry("400x300")
titlos=customtkinter.CTkLabel(basikoparathiro, text="Asteroid Deterctor",font=("fixedsys", 20))
titlos.place(x=270,y=40,anchor="n")
logoauth=customtkinter.CTkImage(light_image= Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo_long.png'),
	dark_image=Image.open(r'C:\Users\stavr\OneDrive\Desktop\Physics\Thesis\code\GUIs\logo_long.png'),size=(150,300))
authlog=customtkinter.CTkLabel(basikoparathiro,image=logoauth,text="")
authlog.place(x=0,y=0)
button1= customtkinter.CTkButton(basikoparathiro,text="Track Asteroid",command=open_window_quick_eph)
button1.place(x=270,y=100,anchor="center")
button2=customtkinter.CTkButton(basikoparathiro,text="Plate Solve",command=open_platesolverwindow)
button2.place(x=270,y=140,anchor="center")
button3= customtkinter.CTkButton(basikoparathiro,text="Asteroid Detection",command=open_window_asteroid)
button3.place(x=270,y=180,anchor="center")
basikoparathiro.mainloop()