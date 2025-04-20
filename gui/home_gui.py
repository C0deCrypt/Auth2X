import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button

def open_register():
    print("Register button clicked")

def open_login():
    print("Login button clicked")

def exit_app():
    root.destroy()

# Initialize the root window
root = tk.Tk()
root.title("Auth2X - Welcome")
root.geometry("500x400")
root.configure(bg="#0F0F0F")
root.resizable(False, False)

# Apply dark theme using ttkbootstrap
style = Style(theme="darkly")  # Clean, dark, and modern

# Custom frame to center content
frame = tk.Frame(root, bg="#0F0F0F")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title = tk.Label(
    frame,
    text="Welcome to Auth2X",
    font=("Segoe UI", 22, "bold"),
    fg="#00FFB2",  # Neon aqua
    bg="#0F0F0F"
)
title.pack(pady=(0, 40))

# Button Style Tweaks
btn_width = 25
btn_font = ("Segoe UI", 12, "bold")

# Register Button (Neon Purple)
register_btn = Button(
    frame,
    text="Register",
    bootstyle="primary",  # Solid modern blue
    width=btn_width,
    command=open_register
)
register_btn.pack(pady=10)

# Login Button (Neon Green)
login_btn = Button(
    frame,
    text="Login",
    bootstyle="primary",  # Solid green
    width=btn_width,
    command=open_login
)
login_btn.pack(pady=10)

# Exit Button (Deep Red)
exit_btn = Button(
    frame,
    text="Exit",
    bootstyle="danger",
    width=btn_width,
    command=exit_app
)
exit_btn.pack(pady=10)

# Run the loop
root.mainloop()
