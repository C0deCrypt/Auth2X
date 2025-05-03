import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import mysql.connector
import json
from cryptography.fernet import Fernet
import numpy as np
from skimage.metrics import structural_similarity as ssim

# === Config Paths ===
EXE_PATH = "D:/auth2x/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
SECRET_KEY_PATH = "../config/secret.key"
DB_CONFIG_PATH = "../config/db_config.json"
CONFIG_PATH = "../config/config.json"
FINGERPRINT_DIR = "../fingerprints/"

IMG_WIDTH = 260
IMG_HEIGHT = 300

# === Load Config ===
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
encrypt_enabled = config.get("encrypt_fingerprint", True)

if encrypt_enabled:
    with open(SECRET_KEY_PATH, 'rb') as key_file:
        fernet = Fernet(key_file.read())

with open(DB_CONFIG_PATH, 'r') as f:
    db_config = json.load(f)

def authenticate_user():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Input Error", "Please enter a username.")
        return

    try:
        subprocess.run([EXE_PATH, username + "_live"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Capture Error", f"Fingerprint capture failed.\n\n{e}")
        return

    live_path = os.path.join(FINGERPRINT_DIR, username + "_live.dat")
    if not os.path.exists(live_path):
        messagebox.showerror("Capture Error", "Live fingerprint file not found.")
        return

    with open(live_path, 'rb') as f:
        live_fp = f.read()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data FROM biometric_data 
            WHERE biometric_type = 'fingerprint' 
            AND user_id = (SELECT id FROM users WHERE username = %s)
        """, (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            messagebox.showerror("Login Error", f"No fingerprint found for user '{username}'.")
            return

        stored_raw = result[0]
        stored_fp = fernet.decrypt(stored_raw) if encrypt_enabled else stored_raw

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch fingerprint.\n\n{e}")
        return

    try:
        live_np = np.frombuffer(live_fp, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
        stored_np = np.frombuffer(stored_fp, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))

        live_float = live_np.astype(np.float32) / 255.0
        stored_float = stored_np.astype(np.float32) / 255.0

        score, _ = ssim(live_float, stored_float, data_range=1.0, full=True)
        print(f"[DEBUG] SSIM = {score:.4f}")

        if score > 0.85:
            messagebox.showinfo("Success", f"User '{username}' authenticated successfully.")
        else:
            messagebox.showerror("Failure", "Fingerprint does not match.\nAccess denied.")

    except Exception as match_err:
        messagebox.showerror("Match Error", f"Fingerprint comparison failed.\n\n{match_err}")

# === GUI Setup ===
root = tk.Tk()
root.title("Fingerprint Login")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(root, text="Login", command=authenticate_user).grid(row=1, columnspan=2, pady=15)

root.mainloop()
