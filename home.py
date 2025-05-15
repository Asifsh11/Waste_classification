import tkinter as tk
from tkinter import filedialog
import subprocess
import cv2
import os
import math
import cvzone
from ultralytics import YOLO
import webbrowser
from PIL import Image, ImageTk  # Import for background image handling



# Function to open respective applications
def open_submit_request():
    subprocess.Popen(["python", "user_login_page.py"])

def open_admin_login():
    subprocess.Popen(["python", "admin_login_page.py"])

def run_object_detection():
    subprocess.Popen(["python", "live_garbage_detection.py"])
# Function to run YOLOv8 detection on uploaded video

# Function to exit the application
def exit_app():
    root.destroy()

# Function to open the waste information website
def open_waste_info():
    webbrowser.open("https://www.epa.gov/recycle")  # Replace with the website URL of your choice
l,b=700,500
# Create the main window
root = tk.Tk()
root.title("Waste Classification")
root.resizable(False, False)
root.geometry(f"{l}x{b}")
l,b=700,500
# Load background image
bg_image = Image.open("Images/home_bg2.jpg")  # Load from specified location
bg_image = bg_image.resize((l, b))  # Resize to match window size
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label widget to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover entire window

# Title label
title_label = tk.Label(root, text="A critical review on recyclable waste classification using AI models", 
                       fg="Black", bg="Yellow", font=("Helvetica", 15))
title_label.pack(pady=10)

# Button frame (Updated to remove black spaces and center buttons)
button_frame = tk.Frame(root, bg="#87CEEB")  # Light blue background
button_frame.pack(pady=5, padx=0, fill=tk.X)

# Inner frame to center buttons
inner_frame = tk.Frame(button_frame, bg="#87CEEB")
inner_frame.pack(pady=5)

buttons = [
    ("User Login", open_submit_request),
    ("Admin Login", open_admin_login),
    ("Live Garbage Detection", run_object_detection)  # Opens new window with Upload Button
]

for text, command in buttons:
    btn = tk.Button(inner_frame, text=text, width=18, height=2, command=command,
                    font=("Helvetica", 10), bg="white", fg="black", relief="ridge")
    btn.pack(side=tk.LEFT, padx=10)  # Adds space between buttons

# Exit Button at Bottom-Right
exit_btn = tk.Button(root, text="Close Application", width=15, height=2, command=exit_app, font=("Helvetica", 10), bg="red", fg="white")
exit_btn.pack(side=tk.RIGHT, anchor="se", padx=20, pady=20)

# Bottom label with hyperlink functionality
bottom_label = tk.Label(root, text="Know more about waste", fg="blue", bg="white",
                        font=("Helvetica", 10), cursor="hand2")
bottom_label.pack(side=tk.BOTTOM, pady=10)

# Bind label click event to open the website
bottom_label.bind("<Button-1>", lambda e: open_waste_info())

# Run the application
root.mainloop()
