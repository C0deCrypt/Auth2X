import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import sys
import subprocess
import sv_ttk
import json
import mysql.connector
import numpy as np
from PIL import Image
from cryptography.fernet import Fernet
from skimage.metrics import structural_similarity as ssim

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login")
        # --- Center the window on the screen ---
        window_width = 500
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.configure(bg="#0a0f1d")
        self.root.resizable(False, False)
        self.load_fonts()
        sv_ttk.set_theme("dark")
        self.create_widgets()

    def load_fonts(self):
        self.headline_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=10, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=12)

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#0a0f1d", padx=30, pady=40)
        self.main_frame.pack(expand=True, )

        content_frame = tk.Frame(self.main_frame, bg="#0a0f1d")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        logo_label = tk.Label(content_frame, text="🔐 SECURE LOGIN", font=self.headline_font, fg="#EDEBE8", bg="#0a0f1d", pady=10)
        logo_label.pack(pady=(0, 30), fill="x")

        method_frame = tk.Frame(content_frame, bg="#0a0f1d")
        method_frame.pack(fill="x", pady=(0, 15))
        tk.Label(method_frame, text="AUTHENTICATION METHOD", font=self.label_font, fg="#EDEBE8", bg="#0a0f1d").pack(anchor="w")
        self.auth_method = ttk.Combobox(method_frame, values=["Face Recognition", "Fingerprint Scan"], state="readonly", font=("Segoe UI", 10))
        self.auth_method.set("Fingerprint Scan")
        self.auth_method.pack(fill="x", pady=(8, 0), ipady=3)

        username_frame = tk.Frame(content_frame, bg="#0a0f1d")
        username_frame.pack(fill="x", pady=(0, 25))
        tk.Label(username_frame, text="USERNAME", font=self.label_font, fg="#EDEBE8", bg="#0a0f1d").pack(anchor="w")
        self.username_entry = ttk.Entry(username_frame, font=("Segoe UI", 10))
        self.username_entry.pack(fill="x", pady=(8, 0), ipady=3)

        button_frame = tk.Frame(content_frame, bg="#0a0f1d")
        button_frame.pack(fill="x", pady=(25, 0))
        login_btn = tk.Button(button_frame, text="Authenticate", command=self.authenticate, bg="#42CC7E", fg="#202342", font=self.button_font, bd=0, padx=10, pady=3, activebackground="#36B069", activeforeground="#0a0f1d", relief="flat", cursor="hand2")
        login_btn.pack(pady=10)

    def authenticate(self):
        method = self.auth_method.get()
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Username is required.")
            return

        if method == "Face Recognition":
            from face_authentication.face_auth import authenticate_face
            self.root.withdraw()
            result = authenticate_face(username)
            self.root.deiconify()
            if result:
                self.root.destroy()
                subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "result_gui.py")])
            else:
                messagebox.showerror("Authentication Failed", "Face authentication failed.")
        else:
            try:
                EXE_PATH = "../fingerprint/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
                CONFIG_PATH = "D:/repo/Auth2X/fingerprint/config/config.json"
                DB_CONFIG_PATH = "D:/repo/Auth2X/fingerprint/config/db_config.json"
                SECRET_KEY_PATH = "D:/repo/Auth2X/fingerprint/config/secret.key"
                FINGERPRINT_DIR = "../fingerprint/fingerprints/"
                IMG_WIDTH, IMG_HEIGHT = 260, 300

                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                encrypt_enabled = config.get("encrypt_fingerprint", True)

                if encrypt_enabled:
                    with open(SECRET_KEY_PATH, 'rb') as f:
                        fernet = Fernet(f.read())

                with open(DB_CONFIG_PATH, 'r') as f:
                    db_config = json.load(f)

                subprocess.run([EXE_PATH, username + "_live"], check=True)
                live_path = os.path.join(FINGERPRINT_DIR, username + "_live.dat")
                if not os.path.exists(live_path):
                    raise Exception("Live fingerprint file not found.")

                with open(live_path, 'rb') as f:
                    live_fp = f.read()

                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM biometric_data WHERE biometric_type = 'fingerprint' AND user_id = (SELECT id FROM users WHERE username = %s)", (username,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()

                if not result:
                    raise Exception("No fingerprint found for user.")

                stored_fp = fernet.decrypt(result[0]) if encrypt_enabled else result[0]

                print(f"[DEBUG] Fingerprint sizes: live={len(live_fp)}, stored={len(stored_fp)}")

                live_np = np.frombuffer(live_fp, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
                stored_np = np.frombuffer(stored_fp, dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))

                # Save PNGs
#                Image.fromarray(live_np).save(f"debug_raw_live.png")
#                Image.fromarray(stored_np).save(f"debug_raw_stored.png")

                # SSIM
                score, _ = ssim(live_np.astype(np.float32) / 255.0,
                                stored_np.astype(np.float32) / 255.0,
                                data_range=1.0, full=True)
                print(f"[DEBUG] SSIM = {score:.4f}")

                if score > 0.35:
                    messagebox.showinfo("Success", f"User '{username}' authenticated successfully.")
                    self.root.destroy()
                    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "result_gui.py")])
                else:
                    messagebox.showerror("Failure", "Fingerprint does not match.")

            except Exception as e:
                messagebox.showerror("Authentication Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    if root.tk.call("tk", "windowingsystem") == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    app = LoginGUI(root)
    root.mainloop()