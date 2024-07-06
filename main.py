import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import bcrypt
import smtplib
import ctypes
import winreg as reg
import sys

import pyotp
import threading
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Database setup
conn = sqlite3.connect('usb_manager.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    email TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    timestamp TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
conn.commit()

# Function to send email notifications
def send_notification(user_email, action):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = user_email
    msg['Subject'] = 'USB Port Manager Notification'
    body = f'Action: {action}\nTimestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, user_email, text)
    server.quit()

# Function to disable USB ports
def disable_usb():
    # Implement USB disable functionality here
    log_action("Disabled USB ports")
    send_notification(logged_in_user[4], "Disabled USB ports")

# Function to enable USB ports
def enable_usb():
    # Implement USB enable functionality here
    log_action("Enabled USB ports")
    send_notification(logged_in_user[4], "Enabled USB ports")

# Function to log actions


# Function to disable USB ports
def disable_usb():
    if logged_in_user:
        prompt_for_password('disable')
    else:
        messagebox.showerror("Error", "You must be logged in to disable USB ports.", parent=main_window)

# Function to enable USB ports
def enable_usb():
    if logged_in_user:
        prompt_for_password('enable')
    else:
        messagebox.showerror("Error", "You must be logged in to enable USB ports.", parent=main_window)

# Function to handle user login
def login():
    global logged_in_user
    username = CustomDialog(login_signup_window, "Login", "Enter your username:").result
    password = CustomDialog(login_signup_window, "Login", "Enter your password:").result
    if username and password:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            logged_in_user = user
            if two_factor_auth(login_signup_window):
                messagebox.showinfo("Success", "Logged in successfully.", parent=login_signup_window)
                login_signup_window.destroy()
                create_main_window()
            else:
                messagebox.showerror("Error", "Invalid OTP.", parent=login_signup_window)
        else:
            messagebox.showerror("Error", "Invalid username or password.", parent=login_signup_window)

# Function to handle user signup
def signup():
    username = CustomDialog(login_signup_window, "Sign Up", "Enter a new username:").result
    password = CustomDialog(login_signup_window, "Sign Up", "Enter a new password:").result
    role = CustomDialog(login_signup_window, "Sign Up", "Enter your role (admin/user):").result
    email = CustomDialog(login_signup_window, "Sign Up", "Enter your email:").result
    if username and password and role and email:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)", (username, hashed_password, role, email))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.", parent=login_signup_window)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.", parent=login_signup_window)

# Function to create the login/signup GUI
def create_login_signup_gui():
    global login_signup_window
    login_signup_window = tk.Tk()
    login_signup_window.title("Login/Sign Up")

    login_signup_window.configure(bg='#e0e0e0')
    login_signup_window.geometry('500x300')

    header = tk.Frame(login_signup_window, bg='#4d4d4d', height=50)
    header.pack(side=tk.TOP, fill=tk.X)

    header_label = tk.Label(header, text="Welcome to USB Port Manager", bg='#4d4d4d', fg='white', font=('Arial', 20, 'bold'))
    header_label.pack(pady=10)

    frame = tk.Frame(login_signup_window, padx=20, pady=20, bg='#f0f0f0')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    login_button = tk.Button(frame, text="Login", command=login, width=25, bg='#2196F3', fg='white', font=('Arial', 14, 'bold'))
    login_button.grid(row=0, column=0, pady=20, padx=10, sticky='ew')

    signup_button = tk.Button(frame, text="Sign Up", command=signup, width=25, bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'))
    signup_button.grid(row=1, column=0, pady=20, padx=10, sticky='ew')

    footer = tk.Frame(login_signup_window, bg='#4d4d4d', height=30)
    footer.pack(side=tk.BOTTOM, fill=tk.X)

    footer_label = tk.Label(footer, text="Developed by Team 15", bg='#4d4d4d', fg='white', font=('Arial', 12))
    footer_label.pack(pady=5)

    login_signup_window.mainloop()

# Function to create the main application window
def create_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("USB Port Manager")

    main_window.configure(bg='#e0e0e0')
    main_window.geometry('600x400')

    header = tk.Frame(main_window, bg='#4d4d4d', height=50)
    header.pack(side=tk.TOP, fill=tk.X)

    header_label = tk.Label(header, text="USB Port Manager", bg='#4d4d4d', fg='white', font=('Arial', 20, 'bold'))
    header_label.pack(pady=10)

    frame = tk.Frame(main_window, padx=20, pady=20, bg='#f0f0f0')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    enable_button = tk.Button(frame, text="Enable USB Ports", command=enable_usb, width=25, bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'))
    enable_button.grid(row=0, column=0, pady=20, padx=10, sticky='ew')

    disable_button = tk.Button(frame, text="Disable USB Ports", command=disable_usb, width=25, bg='#f44336', fg='white', font=('Arial', 14, 'bold'))
    disable_button.grid(row=1, column=0, pady=20, padx=10, sticky='ew')

    log_button = tk.Button(frame, text="View Log", command=show_log_window, width=25, bg='#2196F3', fg='white', font=('Arial', 14, 'bold'))
    log_button.grid(row=2, column=0, pady=20, padx=10, sticky='ew')

    footer = tk.Frame(main_window, bg='#4d4d4d', height=30)
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    footer_label = tk.Label(footer, text="Developed by Team 15", bg='#4d4d4d', fg='white', font=('Arial', 12))
    footer_label.pack(pady=5)

    main_window.mainloop()

# Function to handle USB port scheduling
def schedule_usb_action(action, time_delay):
    def delayed_action():
        time.sleep(time_delay)
        if action == 'enable':
            enable_usb()
        elif action == 'disable':
            disable_usb()

    threading.Thread(target=delayed_action).start()

# Function to handle two-factor authentication (2FA)
def two_factor_auth():
    totp = pyotp.TOTP('your_generated_base32_secret')  # Replace with your secure base32 secret
    otp = totp.now()
    # Send OTP to user's email or phone
    # For simplicity, we'll just print it here
    print(f"Your OTP is: {otp}")
    entered_otp = CustomDialog(main_window, "Two-Factor Authentication", "Enter the OTP sent to your email/phone:").result
    return entered_otp == otp

# Function to handle user login
def login():
    global logged_in_user
    username = CustomDialog(login_signup_window, "Login", "Enter your username:").result
    password = CustomDialog(login_signup_window, "Login", "Enter your password:").result
    if username and password:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            logged_in_user = user
            if two_factor_auth():
                messagebox.showinfo("Success", "Logged in successfully.", parent=login_signup_window)
                login_signup_window.destroy()
                create_main_window()
            else:
                messagebox.showerror("Error", "Invalid OTP.", parent=login_signup_window)
        else:
            messagebox.showerror("Error", "Invalid username or password.", parent=login_signup_window)

# Function to handle user signup
def signup():
    username = CustomDialog(login_signup_window, "Sign Up", "Enter a new username:").result
    password = CustomDialog(login_signup_window, "Sign Up", "Enter a new password:").result
    role = CustomDialog(login_signup_window, "Sign Up", "Enter your role (admin/user):").result
    email = CustomDialog(login_signup_window, "Sign Up", "Enter your email:").result  # New email input
    if username and password and role and email:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)", (username, hashed_password, role, email))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.", parent=login_signup_window)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.", parent=login_signup_window)

# Custom Dialog class for larger input dialogs
class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt, font=('Arial', 14)).pack(pady=10)
        self.entry = tk.Entry(master, show='*', font=('Arial', 14))
        self.entry.pack(pady=10, padx=10)
        self.geometry("400x200")

    def apply(self):
        self.result = self.entry.get()

if __name__ == "__main__":
    logged_in_user = None
    restart_as_admin()
    create_login_signup_gui()
