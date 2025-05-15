import subprocess
from tkinter import messagebox, Tk, filedialog, Label, Entry, Button, StringVar
import cv2
import pymysql
import credentials as cr
import os
#from user_login_page import logged_in_email as le

# Initialize the main window
main = Tk()
main.title("User Request Form")
main.geometry("600x450")
main.config(bg="#2C3E50") # Dark Blue-Gray Background

#print("Logged in Email:", le)

#username = le

# Define StringVars for entry fields
name = StringVar()#name = StringVar(value=username)
location = StringVar()
desc = StringVar()
photo = StringVar()

# Function to upload an image file
def upload():
    global path
    path = filedialog.askopenfilename(initialdir="images")
    photo.set(path)

# Function to save the form data to MySQL and process the image
def save():
    try:
        # Connect to MySQL
        connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
        cur = connection.cursor()

        # Insert data into MySQL table
        cur.execute("INSERT INTO reso (user, location, description, image) VALUES (%s, %s, %s, %s)", 
                    (name.get(), location.get(), desc.get(), photo.get()))
        connection.commit()

        # Get the last inserted ID
        cur.execute("SELECT LAST_INSERT_ID()")
        last_id = cur.fetchone()[0]

        connection.close()

        # Save image locally
        img = cv2.imread(photo.get())
        image_filename = os.path.basename(photo.get())
        save_path = f"Results/{image_filename}"
        cv2.imwrite(save_path, img)

        # Run garbage detection script and get status
        detection_status = process_image(photo.get())

        # Show success message with request ID
        messagebox.showinfo("Request Submitted", f"Request has been submitted. Your request ID is: {last_id}")

        # Open GUI to display images and status
        open_result_gui(photo.get(), detection_status)

    except Exception as es:
        messagebox.showerror("Error", f"Error due to: {es}")

# Function to process image using YOLO and save the result
def process_image(image_path):
    import cvzone
    import math
    from ultralytics import YOLO

    # Load YOLO model with custom weights
    yolo_model = YOLO("Weights/best.pt")
    class_labels = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

    # Load the image
    img = cv2.imread(image_path)

    # Perform object detection
    results = yolo_model(img)

    detected = False  # Default status

    # Loop through detections and draw bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if conf > 0.3:
                detected = True
                cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                cvzone.putTextRect(img, f'{class_labels[cls]} {conf}', (x1, y1 - 10), scale=0.8, thickness=1, colorR=(255, 0, 0))

    # Save the processed image
    result_dir = "Results"
    os.makedirs(result_dir, exist_ok=True)
    image_filename = os.path.basename(image_path)
    result_path = os.path.join(result_dir, image_filename)
    cv2.imwrite(result_path, img)

    # Return detection status
    return "Garbage Detected" if detected else "Garbage Not Detected"

# Function to open result GUI with detection status
def open_result_gui(original_image, status):
    subprocess.Popen(["python", "waste_detection_page.py", original_image, status])

# UI Components
font = ('times', 16, 'bold')
title = Label(main, text='REQUEST YOUR SERVICE', justify='center', bg="#E74C3C", fg="white", font=font, height=2, width=50)       
title.place(x=0, y=10)

font1 = ('times', 14, 'bold')

# Labels & Entry Fields
Label(main, text="Username:", font=font1, bg="#2C3E50", fg="white").place(x=100, y=100)
email_entry = Entry(main, textvariable=name, font=("Arial", 12), width=30)
email_entry.place(x=250, y=100)

Label(main, text="Location:", font=font1, bg="#2C3E50", fg="white").place(x=100, y=150)
Entry(main, textvariable=location, font=("Arial", 12), width=30).place(x=250, y=150)

Label(main, text="Description:", font=font1, bg="#2C3E50", fg="white").place(x=100, y=200)
Entry(main, textvariable=desc, font=("Arial", 12), width=30).place(x=250, y=200)

Label(main, text="Photo Path:", font=font1, bg="#2C3E50", fg="white").place(x=100, y=250)
Entry(main, textvariable=photo, font=("Arial", 12), width=30).place(x=250, y=250)

# Buttons with Colors & Adjusted Positions
Button(main, text="Upload Photo", command=upload, font=font1, bg="#3498DB", fg="white", width=15).place(x=250, y=300)
Button(main, text="Save Request", command=save, font=font1, bg="#2ECC71", fg="white", width=15).place(x=250, y=350)

main.mainloop()

