import tkinter as tk
from tkinter import filedialog
import subprocess
import cv2
import math
import cvzone
from ultralytics import YOLO
from PIL import Image, ImageTk  # Import for background image handling

# Function to run YOLOv8 detection on uploaded video
def run_object_detection(video_path):
    cap = cv2.VideoCapture(video_path)

    # Load YOLO model with custom weights
    model = YOLO("Weights/best.pt")

    # Define class names
    classNames = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

    frame_skip = 15 # Skip every 2nd frame for speed
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success:
            break  # Break the loop if video ends

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip this frame for faster processing

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                if conf > 0.1:
                    cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

        cv2.imshow("Live Garbage Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to upload video and start detection
def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if file_path:
        run_object_detection(file_path)

# Function to open a new page for Live Garbage Detection with Upload Button
def open_live_detection():
    new_window = tk.Tk()
    new_window.title("Live Garbage Detection")
    new_window.geometry("400x300")

    label = tk.Label(new_window, text="Live Garbage Detection Page", font=("Helvetica", 14))
    label.pack(pady=20)

    # Upload Video Button
    upload_btn = tk.Button(new_window, text="Upload Video", font=("Helvetica", 10), command=upload_video)
    upload_btn.pack(pady=10)

    new_window.mainloop()

# Run Live Detection Window
if __name__ == "__main__":
    open_live_detection()
