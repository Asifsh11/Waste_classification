from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import credentials as cr
import subprocess
import os
from PIL import Image, ImageTk  # Correct import for Pillow


class AdminLoginPage:
    def __init__(self, root):
        self.window = root
        self.window.title("Admin Login")
        
        # Apply golden ratio dimensions
        width = 1080
        height = int(width / 1.618)  # Applying golden ratio
        
        self.window.geometry(f"{width}x{height}+100+50")
        self.window.resizable(False, False)  # Disable resizing
        self.window.config(bg="white")

        # Left Frame (Sky Blue)
        self.frame1 = Frame(self.window, bg="#87CEEB")
        self.frame1.place(x=0, y=0, width=int(width * 0.3), height=height)

        Label(self.frame1, text="Admin", font=("times new roman", 40, "bold"), bg="#87CEEB", fg="black").place(x=80, y=int(height * 0.35))
        Label(self.frame1, text="Login", font=("times new roman", 40, "bold"), bg="#87CEEB", fg="black").place(x=80, y=int(height * 0.45))

        # Right Frame (Light Gray)
        self.frame2 = Frame(self.window, bg="#eef2ed")
        self.frame2.place(x=int(width * 0.3), y=0, width=int(width * 0.7), height=height)

        # Load and Set Background Image for Right Section
        self.bg_image = Image.open("Images/admin_bg1.jpg")  # Change path to your actual image
        self.bg_image = self.bg_image.resize((int(width * 0.7), height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.frame2, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame3 = Frame(self.frame2, bg="white")
        self.frame3.place(x=int(width * 0.15), y=int(height * 0.2), width=int(width * 0.4), height=int(height * 0.6))

        Label(self.frame3, text="Name", font=("helvetica", 20, "bold"), bg="white", fg="gray").place(x=50, y=40)
        self.email_entry = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray")
        self.email_entry.place(x=50, y=80, width=int(width * 0.3))

        Label(self.frame3, text="Password", font=("helvetica", 20, "bold"), bg="white", fg="gray").place(x=50, y=120)
        self.password_entry = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray", show="*")
        self.password_entry.place(x=50, y=160, width=int(width * 0.3))

        Button(self.frame3, text="Log In", command=self.login_func, font=("times new roman", 15, "bold"), bd=0, cursor="hand2", bg="#397AF5", fg="white").place(x=50, y=200, width=int(width * 0.3))

    def login_func(self):
        if self.email_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT * FROM admin WHERE Name=%s AND Password=%s", (self.email_entry.get(), self.password_entry.get()))
                row = cur.fetchone()
                
                if row is None:
                    messagebox.showerror("Error!", "Invalid Email or Password", parent=self.window)
                else:
                    self.reset_fields()
                    self.window.destroy()
                    subprocess.Popen(["python", "admin_dashboard.py"])
                
                connection.close()
            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.window)
    
    def reset_fields(self):
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = AdminLoginPage(root)
    root.mainloop()
