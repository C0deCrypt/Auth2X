import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import mysql.connector
import json
from cryptography.fernet import Fernet

# === Config Paths ===
EXE_PATH = "D:/auth2x/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
SECRET_KEY_PATH = "../config/secret.key"
DB_CONFIG_PATH = "../config/db_config.json"
FINGERPRINT_DIR = "../fingerprints/"

# === Load Fernet Key ===
with open(SECRET_KEY_PATH, 'rb') as key_file:
    fernet = Fernet(key_file.read())

# === Load DB Config ===
with open(DB_CONFIG_PATH, 'r') as f:
    db_config = json.load(f)

def authenticate_user():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter a username.")
        return

    # === Step 1: Capture live fingerprint ===
    try:
        subprocess.run([EXE_PATH, username + "_live"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Capture Error", f"Live fingerprint capture failed.\n\n{e}")
        return

    live_path = os.path.join(FINGERPRINT_DIR, username + "_live.dat")
    if not os.path.exists(live_path):
        messagebox.showerror("Capture Error", "Live fingerprint file not found.")
        return

    with open(live_path, 'rb') as f:
        live_fp = f.read()

    # === Step 2: Retrieve and decrypt stored fingerprint ===
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database='auth2x'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT data FROM biometric_data WHERE biometric_type = 'fingerprint' AND user_id = (SELECT id FROM users WHERE username = %s)", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            messagebox.showerror("Login Error", f"No fingerprint found for user '{username}'.")
            return

        encrypted_data = result[0]
        stored_fp = fernet.decrypt(encrypted_data)

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch fingerprint.\n\n{e}")
        return

    # === Step 3: Compare (simple byte match — for now) ===
    if live_fp == stored_fp:
        messagebox.showinfo("Success", f"User '{username}' authenticated successfully.")
    else:
        messagebox.showerror("Failure", "Fingerprint does not match.\nAccess denied.")

# === GUI Setup ===
root = tk.Tk()
root.title("Fingerprint Login")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(root, text="Login", command=authenticate_user).grid(row=1, columnspan=2, pady=15)

root.mainloop()
