from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import pymysql
import subprocess
import os
from user_signup_page import SignUp
import credentials as cr

class login_page:
    def __init__(self, root):
        self.window = root
        self.window.title("User Login Page")
        self.user=None
        self.window.resizable(False, False)
        
        # Golden Ratio Dimensions
        width = 1080
        height = int(width / 1.618)  # Applying golden ratio for better aspect
        
        self.window.geometry(f"{width}x{height}+100+50")
        self.window.config(bg="white")

        # Frame for Yellow Left Section
        self.frame1 = Frame(self.window, bg="#87CEEB")
        self.frame1.place(x=0, y=0, width=int(width * 0.3), height=height)

        Label(self.frame1, text="User", font=("times new roman", 40, "bold"), bg="#87CEEB", fg="black").place(x=80, y=int(height * 0.35))
        Label(self.frame1, text="Login", font=("times new roman", 40, "bold"), bg="#87CEEB", fg="black").place(x=80, y=int(height * 0.45))

        # Load and Set Background Image for Right Section
        self.frame2 = Frame(self.window)
        self.frame2.place(x=int(width * 0.3), y=0, width=int(width * 0.7), height=height)

        self.bg_image = Image.open("Images/user_bg.png")
        self.bg_image = self.bg_image.resize((int(width * 0.7), height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.frame2, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Entry Fields & Buttons (Placing Over the Background)
        self.frame3 = Frame(self.frame2, bg="#eef2ed")
        self.frame3.place(x=int(width * 0.15), y=int(height * 0.2), width=int(width * 0.4), height=int(height * 0.6))

        Label(self.frame3, text="Email Address", font=("helvetica", 20, "bold"), bg="#eef2ed", fg="gray").place(x=30, y=20)
        self.email_entry = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray")
        self.email_entry.place(x=30, y=60, width=int(width * 0.3))

        Label(self.frame3, text="Password", font=("helvetica", 20, "bold"), bg="#eef2ed", fg="gray").place(x=30, y=100)
        self.password_entry = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray", show="*")
        self.password_entry.place(x=30, y=140, width=int(width * 0.3))

        Button(self.frame3, text="Log In", command=self.login_func, font=("times new roman", 15, "bold"), bd=0, cursor="hand2", bg="blue", fg="white").place(x=30, y=180, width=int(width * 0.3))

        Button(self.frame3, text="Forgotten password?", command=self.forgot_func, font=("times new roman", 10, "bold"), bd=0, cursor="hand2", bg="#eef2ed", fg="blue").place(x=100, y=230)

        Button(self.frame3, text="Create New Account", command=self.redirect_window, font=("times new roman", 18, "bold"), bd=0, cursor="hand2", bg="#3aa832", fg="white").place(x=(int(width * 0.4) - int(width * 0.3)) // 2, y=270, width=int(width * 0.25))

    def login_func(self):
        if self.email_entry.get()=="" or self.password_entry.get()=="":
            messagebox.showerror("Error!","All fields are required",parent=self.window)
        else:
            try:
                connection=pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                e,p=self.email_entry.get(),self.password_entry.get()
                cur.execute("select * from user where email=%s and password=%s",e,p)
                row=cur.fetchone()
                #_-----------------
                cur.execute("select f_name from user where email=%s and password=%s",e,p)
                row=cur.fetchone()
                #-------------------

                if row == None:
                    messagebox.showerror("Error!","Invalid USERNAME & PASSWORD",parent=self.window)
                else:
                    self.login_page.user=''
                    subprocess.Popen(["python", "user_dashboard.py"])
                    self.reset_fields()
                    self.window.destroy()
                    connection.close()

            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    def forgot_func(self):
        if self.email_entry.get()=="":
            messagebox.showerror("Error!", "Please enter your Email Id",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("select * from user where email=%s", self.email_entry.get())
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error!", "Email Id doesn't exists")
                else:
                    connection.close()
                    self.root=Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")
                    self.root.focus_force()
                    self.root.grab_set()

            except Exception as e:
                messagebox.showerror("Error", f"{e}")
    
    def redirect_window(self):
        self.window.destroy()
        root = Tk()
        obj = SignUp(root)
        root.mainloop()

    def reset_fields(self):
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)

if __name__ == "__main__":
    root = Tk()
    obj = login_page(root)
    root.mainloop()