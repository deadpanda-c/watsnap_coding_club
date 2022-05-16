#!/bin/python3

import tkinter as tk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk
import os

def make_gif(frame): # DO MANY PICTURES AND MAK A GIF WITH THEM
    global pics
    if pics > 0:
        if pics % 2 == 0:
            cv2.imwrite("myimg" + str(pics) + ".png", frame)
        pics += 1
    if pics == 24:
        os.system("convert -delay 10 myimg*.png mygif.gif")
        os.system("rm *.png")
        pics = 0

def max_rgb_filter(frame): # FUNCTION FOR A ONLY FILTER THAT WILL MAX THE RGB COLOR (SATURATION)
    (B, G, R) = cv2.split(frame)
    M = np.maximum(np.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0
    return cv2.merge([B, G, R])

def verif_nb():
    global filter_choice
    if filter_choice > 3:
        filter_choice = 3
    if filter_choice < 0:
        filter_choice = 0

def apply_filter(frame):
    kernel_5x5 = np.array([ # MATRIX OF THE FINAL WINDOW 
        [-1, -1, -1, -1, -1],
        [-1, 1, 2, 1, -1],
        [-1, 2, 4, 2, -1],
        [-1, 1, 2, 1, -1],
        [-1, -1, -1, -1, -1]
    ])
    verif_nb()
# SELECT THE FILTER TO CHOOSE
    if filter_choice == 1:
        frame = cv2.filter2D(frame, -1, kernel_5x5)
    elif filter_choice == 2:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.Laplacian(gray, cv2.CV_8U, gray, ksize=15)
    elif filter_choice == 3:
        frame = max_rgb_filter(frame)
    return (frame)

# SHOW THE FRAME WITH THE CAMERA OUTPUT AND CONFIG THE FRAME

def show_frame():
    # the var "frame" is an array
    global pics, filter_choice
    _, frame = cap.read() # READ THE CAMERA DATA ( _ IS A TRASH VAR, WE DON'T NEED IT)
    frame = apply_filter(frame)
    make_gif(frame)
    if filter_choice == 0:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # CHAN
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    lmain.imgtk = imgtk
    lmain.configure(image = imgtk)
    lmain.after(20, show_frame)

# SETTING UP THE NEXT FILTER BY PRESSING THE BUTTON

def next_filter():
    global filter_choice
    if filter_choice >= 0:
        filter_choice += 1

# SETTING UP THE PREVIOUS FILTER BY PRESSING THE BUTTON

def prev_filter():
    global filter_choice
    if filter_choice > 0:
        filter_choice -= 1

def take_gif():
    global pics
    pics = 1


# SETTING UP THE FRAME
pics = 0
filter_choice = 0
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#SETTING UP THE WINDOW

"""
var.pack() = display the window item
root.bind() = bind a key to an action
root.attributes() = put the window on fullscreen
var.Label() = init a text on the window
var.Button() = init a button on the window
"""

root = tk.Tk() # INIT THE WINDOW
root.bind("<Escape>", lambda e: root.quit())
root.attributes("-fullscreen", True)
lmain = tk.Label(root)
button3 = tk.Button(root, text="Prendre un GIF", command=take_gif)
button3.pack(side="top")
button = tk.Button(root, text="Filtre Suivant", command=next_filter)
button_bis = tk.Button(root, text="Filtre Précédent", command=prev_filter)
button_bis.pack(side="left")
button.pack(side="right")
lmain.pack(fill="none", expand=True)
show_frame()
root.mainloop() # DISPLAY THE WINDOW
