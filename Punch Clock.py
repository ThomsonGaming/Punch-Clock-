import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from collections import defaultdict

# Function Definitions
def load_user_info():
    """Load user information from a file."""
    try:
        with open("user_info.txt", "r") as file:
            return {line.split(',')[0]: float(line.split(',')[1].strip()) for line in file if ',' in line}
    except FileNotFoundError:
        return {}

def save_user_info(user_info):
    """Save user information to a file."""
    with open("user_info.txt", "w") as file:
        for user_id, hourly_rate in user_info.items():
            file.write(f"{user_id},{hourly_rate}\n")

def add_user():
    """Add a new user or update an existing user's hourly rate."""
    global user_info
    user_info = load_user_info()  # Load user info here to ensure it's defined
    user_id = simpledialog.askstring("Add/Update User", "Enter User ID:")
    if user_id is not None:
        hourly_rate = simpledialog.askfloat("Add/Update User", "Enter Hourly Rate:")
        if hourly_rate is not None:
            user_info[user_id] = hourly_rate
            save_user_info(user_info)
            messagebox.showinfo("User Management", f"User '{user_id}' added/updated with hourly rate of ${hourly_rate}.")

def remove_user():
    """Remove a user from the system."""
    global user_info
    user_info = load_user_info()  # Load user info here to ensure it's defined
    user_id = simpledialog.askstring("Remove User", "Enter User ID to remove:")
    if user_id in user_info:
        del user_info[user_id]
        save_user_info(user_info)
        messagebox.showinfo("User Management", f"User '{user_id}' removed.")
    else:
        messagebox.showerror("User Management", "User not found.")

def access_manager_tools():
    """Prompt for a password and show manager tools upon correct entry."""
    password = simpledialog.askstring("Manager Login", "Enter password:", show='*')
    if password == "admin":  # This is a placeholder password, change as needed
        manager_frame.pack(padx=10, pady=5, fill="both", expand="yes")
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")

def logout_manager():
    """Logout the manager and hide the manager tools frame."""
    manager_frame.pack_forget()

def punch_in():
    """Punch in for a user."""
    user_id = user_id_entry.get()
    if user_id in user_info:
        if user_id not in punch_in_time:
            punch_in_time[user_id] = datetime.datetime.now()
            messagebox.showinfo("Punch In", "Punched in successfully.")
        else:
            messagebox.showwarning("Already Punched In", "You're already punched in.")
    else:
        messagebox.showerror("Invalid User ID", "This user ID does not exist.")

def punch_out():
    """Punch out for a user."""
    user_id = user_id_entry.get()
    if user_id in punch_in_time:
        punch_out_time = datetime.datetime.now()
        duration = punch_out_time - punch_in_time[user_id]
        del punch_in_time[user_id]
        messagebox.showinfo("Punch Out", f"Punched out successfully. Total time: {duration}")
    else:
        messagebox.showerror("Not Punched In", "You're not punched in.")

# Initialize user information
user_info = load_user_info()

# Initialize global variables for punch clock functionality
punch_in_time = {}

# GUI Setup
root = tk.Tk()
root.title("Work Punch Clock System")
root.geometry("400x300")

# User Punch In/Out Frame
user_frame = tk.Frame(root, padx=10, pady=10)
user_frame.pack(padx=10, pady=5)

# User ID entry field and Punch In/Out buttons
tk.Label(user_frame, text="User ID:").grid(row=0, column=0)
user_id_entry = tk.Entry(user_frame)
user_id_entry.grid(row=0, column=1)

tk.Button(user_frame, text="Punch In", command=punch_in).grid(row=1, column=0, sticky="ew")
tk.Button(user_frame, text="Punch Out", command=punch_out).grid(row=1, column=1, sticky="ew")

# Manager Tools Frame (initially hidden)
manager_frame = tk.LabelFrame(root, text="Manager Tools", padx=10, pady=10)

# Manager Tools: Buttons for adding, updating, and removing users
tk.Button(manager_frame, text="Add/Update User", command=add_user).grid(row=0, column=0, sticky="ew", padx=5, pady=2)
tk.Button(manager_frame, text="Remove User", command=remove_user).grid(row=1, column=0, sticky="ew", padx=5)

# Button to logout manager and hide manager tools
tk.Button(manager_frame, text="Logout", command=logout_manager).grid(row=2, column=0, sticky="ew", padx=5, pady=2)

# Button to show manager tools, requiring a password
tk.Button(root, text="Manager Login", command=access_manager_tools).pack(pady=10)

root.mainloop()
