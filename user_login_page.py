from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import pymysql
import subprocess
from user_signup_page import SignUp
import credentials as cr


logged_in_email = None

class login_page:
    def __init__(self, root):
        global logged_in_email  # Declare the global variable
        self.window = root
        self.window.title("User Login Page")
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
        global logged_in_email  # Declare the global variable

        if self.email_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT * FROM user WHERE email=%s AND password=%s", 
                            (self.email_entry.get(), self.password_entry.get()))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error!", "Invalid EMAIL & PASSWORD", parent=self.window)
                else:
                    logged_in_email = self.email_entry.get()  # Store the email globally ✅
                    print("Logged in Email:", logged_in_email)  # Debugging

                    # Start user dashboard
                    subprocess.Popen(["python", "user_dashboard.py"])

                    self.reset_fields()
                    self.window.destroy()

                connection.close()

            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.window)


    def forgot_func(self):
        if self.email_entry.get() == "":
            messagebox.showerror("Error!", "Please enter your Email Id", parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT * FROM user WHERE email=%s", (self.email_entry.get(),))
                row = cur.fetchone()
                
                if row is None:
                    messagebox.showerror("Error!", "Email Id doesn't exist", parent=self.window)
                else:
                    connection.close()
                    
                    # Creating a new Toplevel window for password reset
                    self.root = Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")
                    self.root.focus_force()
                    self.root.grab_set()

                    # Labels & Inputs
                    Label(self.root, text="Change Your Password", font=("times new roman", 20, "bold"), bg="white").place(x=10, y=10)
                    Label(self.root, text="It's quick and easy", font=("times new roman", 12), bg="white").place(x=10, y=45)

                    Label(self.root, text="Select your security question", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=85)

                    self.sec_ques = ttk.Combobox(self.root, font=("times new roman", 13), state='readonly', justify=CENTER)
                    self.sec_ques['values'] = ("Select", "What's your pet's name", "Your first teacher's name", "Your birthplace", "Your favorite movie")
                    self.sec_ques.place(x=10, y=120, width=270)
                    self.sec_ques.current(0)

                    Label(self.root, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=160)
                    self.ans = Entry(self.root, font=("arial"))
                    self.ans.place(x=10, y=195, width=270)

                    Label(self.root, text="New Password", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=235)
                    self.new_pass = Entry(self.root, font=("arial"), show="*")
                    self.new_pass.place(x=10, y=270, width=270)

                    # Submit Button
                    Button(self.root, text="Submit", command=self.change_pass, font=("times new roman", 18, "bold"), bd=0, cursor="hand2", bg="green2", fg="white").place(x=95, y=340, width=200)

            except Exception as e:
                messagebox.showerror("Error", f"{e}", parent=self.window)
    def change_pass(self):
        if self.email_entry.get() == "" or self.sec_ques.get() == "Select" or self.ans.get() == "" or self.new_pass.get() == "":
            messagebox.showerror("Error!", "Please fill all the fields correctly", parent=self.root)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                cur = connection.cursor()
                cur.execute("SELECT question, answer FROM user WHERE email=%s", (self.email_entry.get(),))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error!", "Email not found", parent=self.root)
                else:
                    db_question, db_answer = row  # Get the stored security question & answer
                    print(f"Stored Question: {db_question}, Stored Answer: {db_answer}")  # Debugging output
                    print(f"User Selected Question: {self.sec_ques.get()}, User Answer: {self.ans.get()}")

                    if db_question.strip() != self.sec_ques.get().strip():  
                        messagebox.showerror("Error!", "Selected security question does not match", parent=self.root)
                    elif db_answer.strip().lower() != self.ans.get().strip().lower():  
                        messagebox.showerror("Error!", "Incorrect security answer", parent=self.root)
                    else:
                        cur.execute("UPDATE user SET password=%s WHERE email=%s", (self.new_pass.get(), self.email_entry.get()))
                        connection.commit()
                        messagebox.showinfo("Successful", "Password has been changed successfully", parent=self.root)
                        connection.close()
                        self.root.destroy()

            except Exception as err:
                messagebox.showerror("Error!", f"{err}", parent=self.root)



    
    def redirect_window(self):
        self.window.destroy()
        root = Tk()
        obj = SignUp(root)
        root.mainloop()

    def reset_fields(self):
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)
    def le():
        return logged_in_email

if __name__ == "__main__":
    root = Tk()
    obj = login_page(root)
    root.mainloop()