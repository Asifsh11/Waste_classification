import tkinter as tk
from PIL import Image, ImageTk
import sys

# Get image paths from arguments
if len(sys.argv) > 2:
    original_image = sys.argv[1]
    processed_image = f"Results/{original_image.split('/')[-1]}"
    detection_status = sys.argv[2]  # Get detection status from argument
else:
    original_image = "default.jpg"
    processed_image = "default_result.jpg"
    detection_status = "Unknown"

# Function to load and display images
def load_image(image_path, label):
    try:
        img = Image.open(image_path)
        img = img.resize((400, 300))  
        img_tk = ImageTk.PhotoImage(img)

        label.config(image=img_tk)
        label.image = img_tk  
    except Exception:
        label.config(text="Image not found", font=("Helvetica", 12), bg="white")

# Function to close the application
def close_app():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Waste Classification GUI")
root.geometry("1000x700")  # Adjusted height for better proportions
root.configure(bg="#D6EAF8")  # Light Blue-Gray Background

# Title Label (Updated with Styling)
title_label = tk.Label(root, text="Waste Classification Results", bg="#34495E", fg="white",
                       font=("Helvetica", 20, "bold"), height=2, width=50)
title_label.pack(pady=10)

# Frame for images
image_frame = tk.Frame(root, bg="#D6EAF8")
image_frame.pack(pady=20)

# Left Image Frame (Original Image)
left_frame = tk.Frame(image_frame, bg="white", relief="raised", bd=3)
left_frame.pack(side=tk.LEFT, padx=30)
left_label = tk.Label(left_frame, width=400, height=300, bg="white")
left_label.pack()
load_image(original_image, left_label)

# Right Image Frame (Processed Image)
right_frame = tk.Frame(image_frame, bg="white", relief="raised", bd=3)
right_frame.pack(side=tk.LEFT, padx=30)
right_label = tk.Label(right_frame, width=400, height=300, bg="white")
right_label.pack()
load_image(processed_image, right_label)

# Display Detection Status (Updated Styling)
status_label = tk.Label(root, text=f"Detection Status: {detection_status}", bg="#D6EAF8", fg="red",
                        font=("Helvetica", 16, "bold"))
status_label.pack(pady=10)

# Text Sections (Updated Fonts & Alignment)
text_label1 = tk.Label(root, text="Waste Classification using AI, Detecting and categorizing waste materials, Powered by YOLO object detection.", bg="#D6EAF8", font=("Helvetica", 16, "italic"),wraplength=800, justify="center")
text_label1.pack(pady=5)

text_label4 = tk.Label(root, text="Wait for service approval from admin.\nCheck your approval status in USER LOGIN page.",
                       bg="#D6EAF8", font=("Helvetica", 14, "bold"), wraplength=800, justify="center")
text_label4.pack(pady=10)

# Close Button (Bottom Right)
close_button = tk.Button(root, text="Close Application", command=close_app, font=("Helvetica", 14, "bold"), 
                         bg="#34495E", fg="white", padx=20, pady=5, relief="raised")
close_button.pack(side=tk.RIGHT, anchor="se", padx=20, pady=20)

# Run the application
root.resizable(False, False)
root.mainloop()
