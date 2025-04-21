import os
import sys
import tkinter as tk
import subprocess

def open_register():
    print("Register button clicked")
    root.destroy()  # Close current window if needed
    register_path = os.path.join(os.path.dirname(__file__), "register_gui.py")
    subprocess.run([sys.executable, register_path])

def open_login():
    print("Login button clicked")
    root.destroy()
    login_path = os.path.join(os.path.dirname(__file__), "login_gui.py")
    subprocess.run([sys.executable, login_path])

def exit_app():
    root.destroy()

# Initialize the root window
root = tk.Tk()
root.title("Auth2X - Welcome")
root.geometry("500x600")
root.configure(bg="#0a0f1d")
root.resizable(False, False)

# Center frame
frame = tk.Frame(root, bg="#0a0f1d")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title = tk.Label(
    frame,
    text="WELCOME TO AUTH2X",
    font=("Segoe UI", 25, "bold"),
    fg="#EDEBE8",
    bg="#0a0f1d"
)
title.pack(pady=(0, 40))

# Button config
btn_config = {
    "width": 22,
    "font": ("Segoe UI", 12),
    "bg": "#42CC7E",
    "fg": "#202342",
    "activebackground": "#36b371",
    "activeforeground": "#ffffff",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "cursor": "hand2"
}

# Register Button
register_btn = tk.Button(frame, text="Register", command=open_register, **btn_config)
register_btn.pack(pady=10)

# Login Button
login_btn = tk.Button(frame, text="Login", command=open_login, **btn_config)
login_btn.pack(pady=10)

# Exit Button (different color for emphasis)
exit_btn = tk.Button(
    frame,
    text="Exit",
    command=exit_app,
    bg="#ff5c5c",
    fg="#202342",
    activebackground="#cc4444",
    activeforeground="#ffffff",
    width=22,
    font=("Segoe UI", 12),
    relief="flat",
    bd=0,
    cursor="hand2"
)
exit_btn.pack(pady=10)

# Run
root.mainloop()
