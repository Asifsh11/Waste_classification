from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import credentials as cr
import subprocess
import sys

class UserDashboard:
    def __init__(self, root):
        self.window = root
        self.window.title("User Dashboard")
        self.window.geometry("600x450")
        self.window.resizable(False, False)
        self.username='User 👋'
        # Gradient Background
        self.canvas = Canvas(self.window, width=600, height=450)
        self.canvas.pack(fill="both", expand=True)
        self.gradient_bg()

        # Header
        self.header = Label(self.window, text=f"Welcome,{self.username}", font=("Helvetica", 22, "bold"), bg="#03045E", fg="white", pady=10)
        self.header.place(relwidth=1, y=10)

        # User ID Input
        self.id_label = Label(self.window, text="Enter Your ID:", font=("Helvetica", 14, "bold"), bg="#0077B6", fg="white")
        self.id_label.place(x=200, y=80)

        self.id_entry = Entry(self.window, font=("Helvetica", 14), width=20, bg="white", fg="black", bd=2, relief=RIDGE)
        self.id_entry.place(x=180, y=120)

        # Buttons with Modern Style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#0096C7")

        self.approval_btn = ttk.Button(self.window, text="🔍 Check Approval Status", style="TButton", command=self.check_approval)
        self.approval_btn.place(x=180, y=180)

        self.submit_btn = ttk.Button(self.window, text="📨 Submit Service Request", style="TButton", command=self.submit_service)
        self.submit_btn.place(x=180, y=240)

        # Logout Button
        self.logout_btn = ttk.Button(self.window, text="🛑 Logout", style="TButton", command=self.logout)
        self.logout_btn.place(x=180, y=300)

        # Button Hover Effects
        self.style.map("TButton",
                       foreground=[("active", "white")],
                       background=[("active", "#023E8A")])

    def gradient_bg(self):
        """ Create a gradient background effect (Blue Shades) """
        for i in range(450):
            color = f"#{(0 + i//8):02X}{(119 + i//10):02X}{(182 + i//10):02X}"  # Blue Gradient
            self.canvas.create_line(0, i, 600, i, fill=color)

    def check_approval(self):
        user_id = self.id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("⚠ Input Error", "Please enter your ID.")
            return
        
        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()

            cur.execute("SELECT approval FROM reso WHERE id=%s", (user_id,))
            result = cur.fetchone()

            if result:
                status = result[0]
                if status is None or status.lower() == "none":
                    messagebox.showinfo("Approval Status", "⌛ Admin has not seen your request yet.")
                elif status.lower() == "yes":
                    messagebox.showinfo("Approval Status", "✅ Your request has been approved!")
                elif status.lower() == "no":
                    messagebox.showinfo("Approval Status", "❌ Your request has not been approved.")
                else:
                    messagebox.showinfo("Approval Status", "⚠ No recent request found.")
            else:
                messagebox.showinfo("Approval Status", "⚠ No request found for this ID.")

            connection.close()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Database Error: {e}")

    def submit_service(self):
        """ Opens another Python file for submitting a service request. """
        try:
            subprocess.Popen([sys.executable, "user_request_form.py"])  # Opens "hope.py" in Python
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to open request form: {e}")

    def logout(self):
        """ Logs out the user with confirmation. """
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.window.destroy()  # Closes the application

if __name__ == "__main__":
    root = Tk()
    app = UserDashboard(root)
    root.mainloop()
