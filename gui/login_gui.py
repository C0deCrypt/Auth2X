import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import sys
import subprocess
import sv_ttk


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login")
        self.root.geometry("500x600")
        self.root.configure(bg="#0a0f1d")
        self.root.resizable(False, False)


        # Load custom fonts
        self.load_fonts()
        sv_ttk.set_theme("dark")
        self.create_widgets()



    def load_fonts(self):
        try:
            self.headline_font = font.Font(family="Segoe UI", size=24, weight="bold")
        except:
            self.headline_font = font.Font(family="Helvetica", size=24, weight="bold")

        try:
            self.label_font = font.Font(family="Segoe UI", size=10, weight="bold")
        except:
            self.label_font = font.Font(family="Helvetica", size=10, weight="bold")

        try:
            self.button_font = font.Font(family="Segoe UI", size=12, weight=1 )
        except:
            self.button_font = font.Font(family="Helvetica", size=12)

    def create_widgets(self):
        # Main container - now uses grid for better resizing
        self.main_frame = tk.Frame(self.root, bg="#0a0f1d", padx=30, pady=40)
        self.main_frame.pack(expand=True, fill="both")

        # Make the frame's grid expand
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Inner frame for content with proportional padding
        content_frame = tk.Frame(self.main_frame, bg="#0a0f1d")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Header
        logo_label = tk.Label(
            content_frame,
            text="🔒 SECURE ACCESS",
            font=self.headline_font,
            fg="#EDEBE8",
            bg="#0a0f1d",
            pady=10
        )
        logo_label.pack(pady=(0, 30), fill="x")

        # Authentication method dropdown
        method_frame = tk.Frame(content_frame, bg="#0a0f1d")
        method_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            method_frame,
            text="AUTHENTICATION METHOD",
            font=self.label_font,
            fg="#EDEBE8",
            bg="#0a0f1d"
        ).pack(anchor="w")

        self.auth_method = ttk.Combobox(
            method_frame,
            values=["Face Recognition", "Fingerprint Scan"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.auth_method.set("Face Recognition")
        self.auth_method.pack(fill="x", pady=(8, 0), ipady=3)

        # Username input
        username_frame = tk.Frame(content_frame, bg="#0a0f1d")
        username_frame.pack(fill="x", pady=(0, 25))

        tk.Label(
            username_frame,
            text="USERNAME",
            font=self.label_font,
            fg="#EDEBE8",
            bg="#0a0f1d"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(
            username_frame,
            font=("Segoe UI", 10)
        )
        self.username_entry.pack(fill="x", pady=(8, 0), ipady=3)

        # Login button - centered and responsive
        button_frame = tk.Frame(content_frame, bg="#0a0f1d")
        button_frame.pack(fill="x", pady=(25, 0))

        login_btn = tk.Button(
            button_frame,
            text="Authenticate",
            command=self.authenticate,
            bg="#42CC7E",
            fg="#202342",
            font=self.button_font,
            bd=0,
            padx=10,
            pady=3,
            activebackground="#36B069",
            activeforeground="#0a0f1d",
            relief="flat",
            cursor="hand2"
        )
        login_btn.pack(pady=10)

        # Hover effects
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#4BDF8B"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#42CC7E"))

        # Footer
        footer_frame = tk.Frame(content_frame, bg="#0a0f1d")
        footer_frame.pack(fill="x", pady=(30, 0))

        tk.Label(
            footer_frame,
            text="Select method and enter credentials",
            font=("Segoe UI", 8),
            fg="#A0A0C0",
            bg="#0a0f1d"
        ).pack(anchor="center")

        # Add some empty space at bottom that expands
        tk.Frame(content_frame, bg="#0a0f1d", height=20).pack(fill="x", expand=True)

    def authenticate(self):
        method = self.auth_method.get()
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Username required")
            return

        if method == "Face Recognition":
            from face_authentication.face_auth import authenticate_face
            self.root.withdraw()
            result = authenticate_face(username)
            self.root.deiconify()
            if result:
                self.root.destroy()
                result_path = os.path.join(os.path.dirname(__file__), "result_gui.py")
                subprocess.run([sys.executable, result_path])
            else:
                messagebox.showerror("Authentication Failed", "Face authentication failed.")

        else:
            messagebox.showinfo("Authentication", f"Initiating fingerprint scan for {username}")


if __name__ == "__main__":
    root = tk.Tk()

    # Windows-specific settings for better font rendering
    if root.tk.call("tk", "windowingsystem") == "win32":
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    app = LoginGUI(root)
    root.mainloop()