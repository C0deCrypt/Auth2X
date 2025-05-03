import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import mysql.connector
import json

EXE_PATH = "D:/auth2x/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
STORE_SCRIPT = "../encrypt_store/store_encrypt_data.py"
DB_CONFIG_PATH = "../config/db_config.json"
FINGERPRINT_DIR = "../fingerprints/"

def register_user():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter a username.")
        return

    try:
        conn = mysql.connector.connect(**json.load(open(DB_CONFIG_PATH)))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[INFO] User '{username}' inserted successfully.")
    except Exception as e:
        messagebox.showerror("Registration Error", f"Could not insert user.\n\n{e}")
        return

    try:
        subprocess.run([EXE_PATH, username], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Capture Error", f"Fingerprint capture failed.\n\n{e}")
        return

    try:
        subprocess.run(["python", STORE_SCRIPT, username], check=True)
        messagebox.showinfo("Success", "User registered and fingerprint stored.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Storage Error", f"Failed to store fingerprint.\n\n{e}")

# === GUI ===
root = tk.Tk()
root.title("Register Fingerprint")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(root, text="Register", command=register_user).grid(row=1, columnspan=2, pady=15)

root.mainloop()
