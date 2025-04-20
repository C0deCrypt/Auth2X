import tkinter as tk
from tkinter import ttk, messagebox, font
import sv_ttk


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login")
        self.root.geometry("420x550")  # Initial size
        self.root.configure(bg="#202342")
        self.root.resizable(True, True)  # Allow both horizontal and vertical resizing

        # Set minimum window size
        self.root.minsize(380, 500)

        # Bind the resize event
        self.root.bind("<Configure>", self.on_window_resize)

        # Load custom fonts
        self.load_fonts()
        sv_ttk.set_theme("dark")
        self.create_widgets()

    def on_window_resize(self, event):
        # Adjust elements proportionally when window resizes
        width = self.root.winfo_width()

        # Scale fonts based on window width
        base_size = max(10, min(14, int(width / 30)))
        self.headline_font.configure(size=base_size + 10)
        self.label_font.configure(size=base_size - 2)
        self.button_font.configure(size=base_size)

        # Update padding based on window size
        padx_val = max(20, int(width * 0.05))
        self.main_frame.configure(padx=padx_val)

    def load_fonts(self):
        try:
            self.headline_font = font.Font(family="Montserrat", size=24, weight="bold")
        except:
            self.headline_font = font.Font(family="Helvetica", size=24, weight="bold")

        try:
            self.label_font = font.Font(family="Open Sans", size=10, weight="bold")
        except:
            self.label_font = font.Font(family="Helvetica", size=10, weight="bold")

        try:
            self.button_font = font.Font(family="Poppins", size=12, weight="bold")
        except:
            self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

    def create_widgets(self):
        # Main container - now uses grid for better resizing
        self.main_frame = tk.Frame(self.root, bg="#202342", padx=30, pady=40)
        self.main_frame.pack(expand=True, fill="both")

        # Make the frame's grid expand
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Inner frame for content with proportional padding
        content_frame = tk.Frame(self.main_frame, bg="#202342")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Logo/Header - now centered and responsive
        logo_label = tk.Label(
            content_frame,
            text="🔒 SECURE ACCESS",
            font=self.headline_font,
            fg="#EDEBE8",
            bg="#202342",
            pady=10
        )
        logo_label.pack(pady=(0, 30), fill="x")

        # Authentication method dropdown - responsive width
        method_frame = tk.Frame(content_frame, bg="#202342")
        method_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            method_frame,
            text="AUTHENTICATION METHOD",
            font=self.label_font,
            fg="#EDEBE8",
            bg="#202342"
        ).pack(anchor="w")

        self.auth_method = ttk.Combobox(
            method_frame,
            values=["Face Recognition", "Fingerprint Scan"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.auth_method.set("Face Recognition")
        self.auth_method.pack(fill="x", pady=(8, 0), ipady=5)

        # Username input - responsive width
        username_frame = tk.Frame(content_frame, bg="#202342")
        username_frame.pack(fill="x", pady=(0, 25))

        tk.Label(
            username_frame,
            text="USERNAME",
            font=self.label_font,
            fg="#EDEBE8",
            bg="#202342"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(
            username_frame,
            font=("Segoe UI", 11)
        )
        self.username_entry.pack(fill="x", pady=(8, 0), ipady=8)

        # Login button - centered and responsive
        button_frame = tk.Frame(content_frame, bg="#202342")
        button_frame.pack(fill="x", pady=(25, 0))

        login_btn = tk.Button(
            button_frame,
            text="AUTHENTICATE",
            command=self.authenticate,
            bg="#42CC7E",
            fg="#202342",
            font=self.button_font,
            bd=0,
            padx=30,
            pady=12,
            activebackground="#36B069",
            activeforeground="#202342",
            relief="flat",
            cursor="hand2"
        )
        login_btn.pack(pady=10)

        # Hover effects
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#4BDF8B"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#42CC7E"))

        # Footer - responsive
        footer_frame = tk.Frame(content_frame, bg="#202342")
        footer_frame.pack(fill="x", pady=(30, 0))

        tk.Label(
            footer_frame,
            text="Select method and enter credentials",
            font=("Segoe UI", 8),
            fg="#A0A0C0",
            bg="#202342"
        ).pack(anchor="center")

        # Add some empty space at bottom that expands
        tk.Frame(content_frame, bg="#202342", height=20).pack(fill="x", expand=True)

    def authenticate(self):
        method = self.auth_method.get()
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Username required")
            return

        if method == "Face Recognition":
            messagebox.showinfo("Authentication", f"Initiating facial recognition for {username}")
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