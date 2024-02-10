import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime


# Function to load user information from a file
def load_user_info():
    """Load user information from a file.
    
    Reads the user_info.txt file and creates a dictionary mapping user IDs to their hourly rates.
    If the file does not exist, an empty dictionary is returned.
    
    Returns:
        dict: A dictionary where each key is a user ID and each value is the hourly rate.
    """
    user_info = {}
    try:
        with open("user_info.txt", "r") as file:
            for line in file:
                if ',' in line:  # Ensure the line is correctly formatted
                    user_id, hourly_rate = line.strip().split(',')
                    user_info[user_id] = float(hourly_rate)  # Convert string to float for the hourly rate
    except FileNotFoundError:
        # If the file does not exist, proceed without error
        pass
    return user_info


# Function to save user information to a file
def save_user_info(user_info):
    """Save user information to a file.
    
    Writes the user information from the provided dictionary to the user_info.txt file.
    Each line in the file represents a user, formatted as "user_id,hourly_rate".
    
    Args:
        user_info (dict): A dictionary containing user IDs and their hourly rates.
    """
    with open("user_info.txt", "w") as file:
        for user_id, hourly_rate in user_info.items():
            file.write(f"{user_id},{hourly_rate}\n")  # Write each user's info as a new line in the file


# Function to add or update a user
def add_user():
    """Prompt to add a new user or update an existing user's hourly rate.
    
    Uses a dialog to request the user ID and hourly rate from the manager,
    then updates the global user_info dictionary and saves the changes to the file.
    """
    global user_info  # Reference the global dictionary to allow updates
    user_info = load_user_info()  # Ensure we have the latest user info
    user_id = simpledialog.askstring("Add/Update User", "Enter User ID:")
    if user_id is not None:  # Check that user did not cancel the dialog
        hourly_rate = simpledialog.askfloat("Add/Update User", "Enter Hourly Rate:")
        if hourly_rate is not None:  # Ensure a valid rate was entered
            user_info[user_id] = hourly_rate  # Update or add the user's rate
            save_user_info(user_info)  # Save changes to the file
            messagebox.showinfo("User Management", f"User '{user_id}' added/updated with hourly rate of ${hourly_rate}.")


# Function to remove a user
def remove_user():
    """Prompt to remove a user from the system.
    
    Uses a dialog to request the user ID for removal,
    then updates the global user_info dictionary and saves the changes if the user exists.
    """
    global user_info  # Reference the global dictionary to allow updates
    user_info = load_user_info()  # Ensure we have the latest user info
    user_id = simpledialog.askstring("Remove User", "Enter User ID to remove:")
    if user_id in user_info:  # Check if the user exists
        del user_info[user_id]  # Remove the user from the dictionary
        save_user_info(user_info)  # Save changes to the file
        messagebox.showinfo("User Management", f"User '{user_id}' removed.")
    else:
        messagebox.showerror("User Management", "User not found.")


# Function to access manager tools
def access_manager_tools():
    """Prompt for a manager password to access management tools.
    
    If the correct password is entered, the manager tools frame is displayed.
    Otherwise, an error message is shown.
    """
    password = simpledialog.askstring("Manager Login", "Enter password:", show='*')
    if password == "admin":  # Placeholder password, consider using a more secure method in production
        manager_frame.pack(padx=10, pady=5, fill="both", expand="yes")  # Show manager tools
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")


# Function to log out from manager tools
def logout_manager():
    """Hide the manager tools frame, effectively logging out the manager."""
    manager_frame.pack_forget()  # Hide the frame


# Function for a user to punch in
def punch_in():
    """Record the current time as the punch-in time for a user.
    
    Validates the user ID, checks if the user is already punched in,
    and logs the punch-in time to a file.
    """
    user_id = user_id_entry.get()
    if user_id in user_info:
        if user_id not in punch_in_time:
            current_time = datetime.datetime.now()
            punch_in_time[user_id] = current_time
            # Log punch in to file for record-keeping
            with open("time_log.txt", "a") as file:
                file.write(f"{user_id},{current_time},in\n")
            messagebox.showinfo("Punch In", "Punched in successfully.")
        else:
            messagebox.showwarning("Already Punched In", "You're already punched in.")
    else:
        messagebox.showerror("Invalid User ID", "This user ID does not exist.")


# Function for a user to punch out
def punch_out():
    """Record the current time as the punch-out time for a user and calculate the total hours worked.
    
    Validates the user's punch-in status, calculates the duration since punch-in,
    logs the punch-out time, and displays the total hours worked along with the amount owed.
    """
    user_id = user_id_entry.get()
    if user_id in punch_in_time:
        punch_out_time = datetime.datetime.now()
        duration = punch_out_time - punch_in_time[user_id]
        total_hours = duration.total_seconds() / 3600
        amount_owed = total_hours * user_info[user_id]
        # Log punch out to file for record-keeping
        with open("time_log.txt", "a") as file:
            file.write(f"{user_id},{punch_out_time},out\n")
        del punch_in_time[user_id]  # Clear punch-in status
        messagebox.showinfo("Punch Out", f"Punched out successfully. Total time: {duration}, Amount owed: ${amount_owed:.2f}")
    else:
        messagebox.showerror("Not Punched In", "You're not punched in.")


# Function to display a report of total hours worked
def show_time_report():
    """Generate and display a report of total hours worked for each user based on punch-in/out logs.
    
    Reads the time log file, calculates total hours worked for each user, and displays the results.
    Handles cases where the log file might not exist.
    """
    try:
        with open("time_log.txt", "r") as file:
            logs = file.readlines()
        
        user_hours = defaultdict(float)  # Default to 0 for new keys
        temp_punch_in_time = {}  # Temporary storage for punch-in times
        for line in logs:
            user_id, timestamp, status = line.strip().split(',')
            timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            if status == 'in':
                temp_punch_in_time[user_id] = timestamp
            elif status == 'out' and user_id in temp_punch_in_time:
                duration = timestamp - temp_punch_in_time[user_id]
                user_hours[user_id] += duration.total_seconds() / 3600  # Convert seconds to hours
                del temp_punch_in_time[user_id]  # Remove user from temp storage after calculating hours
        
        # Generate and show the report message
        report_message = "User Hours Report:\n" + "\n".join([f"User {uid}: {hours:.2f} hours" for uid, hours in user_hours.items()])
        messagebox.showinfo("Time Report", report_message)
    except FileNotFoundError:
        messagebox.showerror("Error", "Time log file not found.")


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

# Button for showing time report
tk.Button(root, text="Show Time Report", command=show_time_report).pack(pady=10)

root.mainloop()
