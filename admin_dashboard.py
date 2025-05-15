from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import credentials as cr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdminPage:
    def __init__(self, root):
        self.window = root
        self.window.title("Admin Dashboard")

        width = 1080
        height = int(width / 1.618)  

        self.window.geometry(f"{width}x{height}+100+50")
        self.window.resizable(False, False)
        self.window.config(bg="white")

        self.frame1 = Frame(self.window, bg="#87CEEB")
        self.frame1.place(x=0, y=0, width=int(width * 0.3), height=height)

        Label(self.frame1, text="Admin", font=("times new roman", 40, "bold"), bg="#87CEEB", fg="black").place(x=80, y=int(height * 0.1))
        Label(self.frame1, text="Dashboard", font=("times new roman", 30, "bold"), bg="#87CEEB", fg="black").place(x=50, y=int(height * 0.2))

        Button(self.frame1, text="View User Data", font=("times new roman", 15, "bold"), bg="green", fg="white", command=self.view_users).place(x=60, y=int(height * 0.35), width=200, height=40)
        Button(self.frame1, text="View Requests", font=("times new roman", 15, "bold"), bg="orange", fg="white", command=self.view_requests).place(x=60, y=int(height * 0.42), width=200, height=40)
        Button(self.frame1, text="Approval Chart", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.approval_chart).place(x=60, y=int(height * 0.49), width=200, height=40)
        Button(self.frame1, text="Request Chart", font=("times new roman", 15, "bold"), bg="purple", fg="white", command=self.request_chart).place(x=60, y=int(height * 0.56), width=200, height=40)
        Button(self.frame1, text="Logout", font=("times new roman", 15, "bold"), bg="red", fg="white", command=self.logout).place(x=60, y=int(height * 0.7), width=200, height=40)

        # Set up the right frame
        self.frame2 = Frame(self.window, bg="#eef2ed")
        self.frame2.place(x=int(width * 0.3), y=0, width=int(width * 0.7), height=height)

        # Project Title
        Label(self.frame2, text="Welcome to Admin Dashboard", font=("Helvetica", 25, "bold"), bg="#eef2ed", fg="black").place(x=int(width * 0.15), y=int(height * 0.05))

        # Waste Management Project Description
        project_description = """
        This Waste Classification Project utilizes AI-based object detection
        to identify different types of waste materials from images, videos.
        By classifying waste efficiently, it promotes better waste disposal
        practices and contributes to a cleaner environment.
        """
        Label(self.frame2, text=project_description, font=("Helvetica", 12), bg="#eef2ed", fg="black", justify=LEFT, wraplength=500).place(x=40, y=int(height * 0.15))

        # Key Features Title
        Label(self.frame2, text="Key Features:", font=("Helvetica", 14, "bold"), bg="#eef2ed", fg="black").place(x=40, y=int(height * 0.35))

        # Features List
        features = [
            "✔ Detects waste type using AI",
            "✔ Stores user requests in database",
            "✔ Admin can approve or reject requests",
            "✔ Provides data visualization through charts",
            "✔ Helps in efficient waste management"
        ]

        # Displaying Features as Labels
        for i, feature in enumerate(features):
            Label(self.frame2, text=feature, font=("Helvetica", 12), bg="#eef2ed", fg="black").place(x=60, y=int(height * 0.4) + (i * 30))


    def clear_frame2(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

    def view_users(self):
        self.clear_frame2()
        Label(self.frame2, text="User Data", font=("Helvetica", 20, "bold"), bg="#eef2ed", fg="black").pack(pady=10)

        tree = ttk.Treeview(self.frame2, columns=("First Name", "Last Name", "Email"), show="headings")

        # Define column headers and set width
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("Email", text="Email")

        # Set column widths (Adjust as per your need)
        tree.column("First Name", anchor=CENTER, width=150)
        tree.column("Last Name", anchor=CENTER, width=150)
        tree.column("Email", anchor=CENTER, width=200)

        tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("SELECT f_name, l_name, email FROM user")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", END, values=row)
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def view_requests(self):
        self.clear_frame2()
        Label(self.frame2, text="Service Requests", font=("Helvetica", 20, "bold"), bg="#eef2ed", fg="black").pack(pady=10)

        self.tree = ttk.Treeview(self.frame2, columns=("ID", "Location", "Description", "Approval"), show="headings")

        # Define column headers
        self.tree.heading("ID", text="ID")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Approval", text="Approval")

        # Set column widths
        self.tree.column("ID", anchor=CENTER, width=50)
        self.tree.column("Location", anchor=W, width=150)
        self.tree.column("Description", anchor=W, width=300)
        self.tree.column("Approval", anchor=CENTER, width=100)

        self.tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Bind selection event for dropdown placement
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

        # Dropdown for Approval
        self.approval_var = StringVar()
        self.dropdown = ttk.Combobox(self.frame2, textvariable=self.approval_var, values=["Yes", "No", "None"])
        self.dropdown.bind("<<ComboboxSelected>>", self.update_approval)

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("SELECT id, location, description, approval FROM reso")  # Fixed column order
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", END, values=row)
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")



    def on_item_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        values = item["values"]
        
        # Adjust dropdown placement for approval column
        row_bbox = self.tree.bbox(selected_item[0], column=3)
        if row_bbox:
            x, y, width, height = row_bbox
            self.dropdown.place(x=x + 5, y=y + 30, width=width, height=height)
            self.approval_var.set(values[3])  # Set dropdown to selected approval value
            self.selected_id = values[0]


    def update_approval(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return

        # Get selected item's values
        item = self.tree.item(selected_item)
        record_id = item["values"][0]  # Assuming ID is the first column
        new_approval = self.approval_var.get()

        if not new_approval:
            messagebox.showwarning("Warning", "Please select an approval status.")
            return

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("UPDATE reso SET approval = %s WHERE id = %s", (new_approval, record_id))
            connection.commit()
            connection.close()

            # Show success message
            messagebox.showinfo("Success", "Approval updated successfully!")

            # Refresh the table to reflect changes
            self.view_requests()  # Reload data from the database

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")



    def approval_chart(self):
        self.clear_frame2()  # Clear previous content
        Label(self.frame2, text="Approval Status Chart", font=("Helvetica", 20, "bold"), bg="#eef2ed", fg="black").pack(pady=10)

        # Connect to database and fetch counts
        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            cur.execute("SELECT approval, COUNT(*) FROM reso GROUP BY approval")
            data = cur.fetchall()
            connection.close()
            
            # Process data
            counts = {"Yes": 0, "No": 0, "None": 0}  # Default values
            for approval, count in data:
                counts[approval] = count
            
            labels = ["Yes", "No", "None"]
            values = [counts["Yes"], counts["No"], counts["None"]]
            colors = ["green", "red", "gray"]

            # Create Pie Chart
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title("Approval Status Distribution")

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")

    def request_chart(self):
        self.clear_frame2()  # Clear previous content
        Label(self.frame2, text="User Requests Chart", font=("Helvetica", 20, "bold"), bg="#eef2ed", fg="black").pack(pady=10)

        try:
            # Connect to database
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            cur = connection.cursor()
            
            # Fetch requests per username
            cur.execute("SELECT user, COUNT(*) FROM reso GROUP BY user")  
            data = cur.fetchall()
            connection.close()

            # Process data
            users = [row[0] for row in data]  # Usernames
            counts = [row[1] for row in data]  # Request counts

            # Create Bar Chart
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.bar(users, counts, color="#397AF5")
            ax.set_xlabel("Users")
            ax.set_ylabel("Number of Requests")
            ax.set_title("Requests Per User")
            ax.set_xticks(range(len(users)))
            ax.set_xticklabels(users, rotation=30, ha="right", fontsize=10)

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.frame2)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {e}")



    def logout(self):
        self.window.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = AdminPage(root)
    root.mainloop()
