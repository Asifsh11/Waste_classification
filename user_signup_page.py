from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import pymysql, os
import credentials as cr

class SignUp:
    def __init__(self, root):
        self.window = root
        self.window.title("Sign Up")
        self.apply_golden_ratio()
        self.window.config(bg="white")
        self.window.resizable(False, False)

        self.bg_img = self.resize_bg_image("Images/signup_bg.jpg")
        background = Label(self.window, image=self.bg_img)
        background.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.window, bg="#eef2ed")
        frame.place(x=350, y=100, width=500, height=550)

        title1 = Label(frame, text="Sign Up", font=("times new roman", 25, "bold"), bg="#eef2ed").place(x=20, y=10)
        title2 = Label(frame, text="Join with us", font=("times new roman", 13), bg="#eef2ed", fg="gray").place(x=20, y=50)

        Label(frame, text="First name", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=20, y=100)
        Label(frame, text="Last name", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=240, y=100)

        self.fname_txt = Entry(frame, font=("arial"))
        self.fname_txt.place(x=20, y=130, width=200)

        self.lname_txt = Entry(frame, font=("arial"))
        self.lname_txt.place(x=240, y=130, width=200)

        Label(frame, text="Email", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=20, y=180)

        self.email_txt = Entry(frame, font=("arial"))
        self.email_txt.place(x=20, y=210, width=420)

        Label(frame, text="Security questions", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=20, y=260)
        Label(frame, text="Answer", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=240, y=260)

        self.questions = ttk.Combobox(frame, font=("helvetica", 13), state='readonly', justify=CENTER)
        self.questions['values'] = ("Select", "What's your pet name?", "Your first teacher name", "Your birthplace", "Your favorite movie")
        self.questions.place(x=20, y=290, width=200)
        self.questions.current(0)

        self.answer_txt = Entry(frame, font=("arial"))
        self.answer_txt.place(x=240, y=290, width=200)

        Label(frame, text="New password", font=("helvetica", 15, "bold"), bg="#eef2ed").place(x=20, y=340)

        self.password_txt = Entry(frame, font=("arial"))
        self.password_txt.place(x=20, y=370, width=420)

        self.terms = IntVar()
        Checkbutton(frame, text="I Agree The Terms & Conditions", variable=self.terms, onvalue=1, offvalue=0,
                    bg="#eef2ed", font=("times new roman", 12)).place(x=20, y=420)

        self.signup = Button(frame, text="Sign Up", command=self.signup_func, font=("times new roman", 18, "bold"),
                             bd=0, cursor="hand2", bg="red", fg="white")
        self.signup.place(x=80, y=470, width=160)

        self.login_button = Button(frame, text="Login", command=self.redirect_to_login, font=("times new roman", 18, "bold"),bd=0, cursor="hand2", bg="green", fg="white")
        self.login_button.place(x=260, y=470, width=160)
        self.login_button.place_forget()

    def apply_golden_ratio(self):
        width = 1080
        height = int(width / 1.618)
        self.window.geometry(f"{width}x{height}+0+0")

    def resize_bg_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((1080, int(1080 / 1.618)), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def signup_func(self):
        fname = self.fname_txt.get().strip()
        lname = self.lname_txt.get().strip()
        email = self.email_txt.get().strip()
        question = self.questions.get().strip()
        answer = self.answer_txt.get().strip()
        password = self.password_txt.get().strip()

        print(f"DEBUG: fname={fname}, lname={lname}, email={email}, question={question}, answer={answer}, password={password}")

        if not all([fname, lname, email, answer, password]) or question == "Select":
            messagebox.showerror("Error!", "Sorry! All fields are required", parent=self.window)
            return

        if self.terms.get() == 0:
            messagebox.showerror("Error!", "Please Agree with our Terms & Conditions", parent=self.window)
            return

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("SELECT * FROM user WHERE email=%s", email)
            row = cur.fetchone()

            if row:
                messagebox.showerror("Error!", "The email ID already exists, please try again with another email ID", parent=self.window)
            else:
                cur.execute("INSERT INTO user (f_name, l_name, email, question, answer, password) VALUES (%s, %s, %s, %s, %s, %s)",
                            (fname, lname, email, question, answer, password))
                connection.commit()
                connection.close()
                messagebox.showinfo("Congratulations!", "Register Successful", parent=self.window)
                self.show_login_button()
                self.reset_fields()
        except Exception as es:
            messagebox.showerror("Error!", f"Error due to {es}", parent=self.window)

    def show_login_button(self):
        self.login_button.place(x=260, y=470, width=160)

    def reset_fields(self):
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.questions.current(0)
        self.answer_txt.delete(0, END)
        self.password_txt.delete(0, END)

    def redirect_to_login(self):
        self.window.destroy()
        os.system("python user_login_page.py")

if __name__ == "__main__":
    root = Tk()
    obj = SignUp(root)
    root.mainloop()
