import tkinter as tk
from tkinter import ttk, messagebox, font
import sv_ttk
import os
import sys
import subprocess
import mysql.connector
import json
import numpy as np
from PIL import Image

class RegisterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")
        #self.root.geometry("500x600")
        # Set dimensions
        window_width = 500
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
<<<<<<< HEAD
        #self.main_frame.pack(expand=True, fill="both")
        self.main_frame.pack(expand=True)
=======
        self.main_frame.pack(expand=True, fill="both")
>>>>>>> 93b416efcc00f63cf8d96b2611f52628c33a483d

        content_frame = tk.Frame(self.main_frame, bg="#0a0f1d")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        logo_label = tk.Label(content_frame, text="📝 REGISTER USER", font=self.headline_font, fg="#EDEBE8", bg="#0a0f1d", pady=10)
        logo_label.pack(pady=(0, 30), fill="x")

        method_frame = tk.Frame(content_frame, bg="#0a0f1d")
        method_frame.pack(fill="x", pady=(0, 15))
        tk.Label(method_frame, text="REGISTRATION METHOD", font=self.label_font, fg="#EDEBE8", bg="#0a0f1d").pack(anchor="w")
        self.auth_method = ttk.Combobox(method_frame, values=["Face Registration", "Fingerprint Scan"], state="readonly", font=("Segoe UI", 10))
        self.auth_method.set("Face Registration")
        self.auth_method.pack(fill="x", pady=(8, 0), ipady=3)

        username_frame = tk.Frame(content_frame, bg="#0a0f1d")
        username_frame.pack(fill="x", pady=(0, 25))
        tk.Label(username_frame, text="USERNAME", font=self.label_font, fg="#EDEBE8", bg="#0a0f1d").pack(anchor="w")
        self.username_entry = ttk.Entry(username_frame, font=("Segoe UI", 10))
        self.username_entry.pack(fill="x", pady=(8, 0), ipady=3)

        button_frame = tk.Frame(content_frame, bg="#0a0f1d")
        button_frame.pack(fill="x", pady=(25, 0))
        register_btn = tk.Button(button_frame, text="Register", command=self.register_user, bg="#42CC7E", fg="#202342", font=self.button_font, bd=0, padx=10, pady=3, activebackground="#36B069", activeforeground="#0a0f1d", relief="flat", cursor="hand2")
        register_btn.pack(pady=10)

    def register_user(self):
        method = self.auth_method.get()
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Username is required.")
            return

        if method == "Face Registration":
            try:
                from Face_registration.face_registeration import register_face
                self.root.withdraw()
                result = register_face(username)
                self.root.deiconify()
                if result:
                    self.root.destroy()
                    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "login_gui.py")])
                else:
                    messagebox.showerror("Registration Failed", "Face registration failed.")
            except Exception as e:
                messagebox.showerror("Face Registration Error", f"Unexpected error: {e}")
        else:
            try:
                DB_CONFIG_PATH = "../fingerprint/config/db_config.json"
                EXE_PATH = os.path.abspath("../fingerprint/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe")
                STORE_SCRIPT = os.path.abspath("../fingerprint/encrypt_store/store_encrypt_data.py")
                FP_DIR = os.path.abspath("../fingerprint/fingerprints/")
                fp_path = os.path.join(FP_DIR, f"{username}.dat")

                for path in [DB_CONFIG_PATH, EXE_PATH, STORE_SCRIPT]:
                    if not os.path.isfile(path):
                        raise FileNotFoundError(f"Required file not found: {path}")
                if not os.path.isdir(FP_DIR):
                    os.makedirs(FP_DIR)
                    print(f"[INFO] Created missing fingerprint directory at {FP_DIR}")

                with open(DB_CONFIG_PATH, 'r') as f:
                    db_config = json.load(f)
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                conn.commit()
                cursor.close()
                conn.close()
                print(f"[INFO] User '{username}' inserted into database.")

                print("[INFO] Running fingerprint capture EXE...")
                result = subprocess.run([EXE_PATH, username], capture_output=True, text=True)
                print("[STDOUT]:", result.stdout)
                print("[STDERR]:", result.stderr)

                if result.returncode != 0:
                    raise RuntimeError(f"Fingerprint capture failed with code {result.returncode}.")

                if not os.path.exists(fp_path):
                    raise FileNotFoundError(f"Expected fingerprint not found: {fp_path}")

                # Save PNG for debug
                with open(fp_path, 'rb') as f:
                    raw = f.read()
<<<<<<< HEAD
                #img = np.frombuffer(raw, dtype=np.uint8).reshape((300, 260))
                #Image.fromarray(img).save(f"debug_{username}_registered.png")
=======
                img = np.frombuffer(raw, dtype=np.uint8).reshape((300, 260))
                Image.fromarray(img).save(f"debug_{username}_registered.png")
>>>>>>> 93b416efcc00f63cf8d96b2611f52628c33a483d

                print("[INFO] Running fingerprint storage...")
                subprocess.run([sys.executable, STORE_SCRIPT, username], check=True)

                messagebox.showinfo("Success", f"User '{username}' registered successfully.")
                self.root.destroy()
                subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "login_gui.py")])

            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    if root.tk.call("tk", "windowingsystem") == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    app = RegisterGUI(root)
    root.mainloop()
