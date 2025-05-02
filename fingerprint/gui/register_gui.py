import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
import json
import os

# === Load DB config ===
with open('../config/db_config.json', 'r') as f:
    db_config = json.load(f)

# === Absolute Paths ===
EXE_PATH = "D:/auth2x/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
ENCRYPT_SCRIPT = "D:/auth2x/encrypt_store/store_encrypt_data.py"

def register_user():
    username = username_entry.get().strip()
    email = email_entry.get().strip()

    if not username or not email:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        # === Connect to MySQL ===
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database='auth2x'
        )
        cursor = conn.cursor()

        # === Insert or confirm user ===
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            print(f"[INFO] User '{username}' already exists with ID {result[0]}")
        else:
            cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
            conn.commit()
            print(f"[INFO] User '{username}' inserted successfully.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as db_err:
        messagebox.showerror("Database Error", f"Could not connect or insert user:\n{db_err}")
        return

    # === Call fingerprint capture exe ===
    try:
        if not os.path.exists(EXE_PATH):
            messagebox.showerror("Path Error", f"Fingerprint EXE not found:\n{EXE_PATH}")
            return

        print(f"[DEBUG] Running: {EXE_PATH} {username}")
        subprocess.run([EXE_PATH, username], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Capture Error", f"Fingerprint capture failed.\n\n{e}")
        return

    # === Call encrypt & store Python script ===
    try:
        if not os.path.exists(ENCRYPT_SCRIPT):
            messagebox.showerror("Path Error", f"Encrypt script not found:\n{ENCRYPT_SCRIPT}")
            return

        print(f"[DEBUG] Encrypting fingerprint using: {ENCRYPT_SCRIPT}")
        subprocess.run(["python", ENCRYPT_SCRIPT, username], check=True)
        messagebox.showinfo("Success", f"User '{username}' registered and fingerprint stored.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Storage Error", f"Fingerprint storage failed.\n\n{e}")
        return

# === GUI Setup ===
root = tk.Tk()
root.title("User Registration")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=5)

username_entry = tk.Entry(root, width=30)
email_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10)
email_entry.grid(row=1, column=1, padx=10)

tk.Button(root, text="Register", command=register_user).grid(row=2, columnspan=2, pady=15)

root.mainloop()
