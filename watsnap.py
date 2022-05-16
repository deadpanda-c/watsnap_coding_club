import pickletools
import tkinter as tk
import numpy as np
import cv2
import time
import os
from PIL import Image, ImageTk

def show_frame():

    global pics, filter_choice

    _, frame = cap.read()
    frame = apply_filter(frame)
    if filter_choice == 0 :
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    lmain.imgtk = imgtk
    lmain.configure(image = imgtk)
    lmain.after(20, show_frame)

def prev_filter():
    global filter_choice
    if filter_choice > 0:
        filter_choice -= 1

def next_filter():
    global filter_choice
    if filter_choice >= 0 :
        filter_choice += 1

def max_rgb_filter(frame) :
    (B,G,R) = cv2.split(frame)
    M = np.maximum(np.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0
    return cv2.merge([B, G, R])

def apply_filter(frame):
    kernel_5x5 = np.array([
    [-1, -1, -1, -1, -1],
    [-1, 1, 2, 1, -1],
    [-1, 2, 4, 2, -1],
    [-1, 1, 2, 1, -1],
    [-1, -1, -1, -1, -1]
    ])
    prev_filter()
    if filter_choice == 1:
        frame = cv2.filter2D(frame, -1, kernel_5x5)
    elif filter_choice == 2 :
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.Laplacian(gray, cv2.CV_8U, gray, ksize=15)
    elif filter_choice == 3:
        frame = max_rgb_filter(frame)
    return (frame)

filter_choice = 0

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


window = tk.Tk()
window.bind("<Escape>", lambda e: window.quit())
window.attributes("-fullscreen", True)

button = tk.Button(window, text="Filtre Suivant", command=next_filter)
button.pack(side="right")


button = tk.Button(window, text="Filtre Précédent", command=prev_filter)
button.pack(side="left")

lmain = tk.Label(window)
lmain.pack(fill="none", expand=True)
show_frame()
window.mainloop()
