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
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Username is required.")
            return

        try:
            exe_path = "../fingerprint/capture/CaptureFingerprint/x64/Debug/CaptureFingerprint.exe"
            match_script = os.path.abspath("../fingerprint/match template.py")

            subprocess.run([exe_path, username + "_live"], check=True)
            if not os.path.exists(f"D:/repo/Auth2X/fingerprint/fingerprints/{username}_live.dat"):
                raise Exception("Live fingerprint file not found.")

            result = subprocess.run(
                [sys.executable, match_script, username],
                capture_output=True, text=True
            )

            output = result.stdout.strip()
            print("[DEBUG] Matcher Output:\n", output)

            if "AUTH_SUCCESS" in output:
                messagebox.showinfo("Success", f"User '{username}' authenticated successfully.")
                self.root.destroy()
                subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "result_gui.py")])
            elif "AUTH_FAIL" in output:
                messagebox.showerror("Authentication Failed", "Fingerprint does not match.")
            else:
                messagebox.showerror("Matcher Error", output)

        except Exception as e:
            messagebox.showerror("Authentication Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    if root.tk.call("tk", "windowingsystem") == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    app = LoginGUI(root)
    root.mainloop()