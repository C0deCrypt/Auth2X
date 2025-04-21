import tkinter as tk

# Setup main window
root = tk.Tk()
root.title("Login Successful")
root.geometry("500x300")
root.configure(bg="#0a0f1d")  # Deep navy blue background

# Font colors and style
primary_color = "#00ff99"  # Mint green glow
accent_color = "#1f2833"   # Soft blackish background for contrast
font_title = ("Segoe UI", 24, "bold")
font_button = ("Segoe UI", 12)

# Title label
title_label = tk.Label(
    root,
    text="ACCESS GRANTED",
    font=font_title,
    fg=primary_color,
    bg="#0a0f1d"
)
title_label.pack(pady=60)

# Message
msg_label = tk.Label(
    root,
    text="Welcome to the system!",
    font=("Helvetica", 14),
    fg="white",
    bg="#0a0f1d"
)
msg_label.pack()

# Close button
def close_window():
    root.destroy()

close_btn = tk.Button(
    root,
    text="Close",
    font=font_button,
    bg=primary_color,
    fg="black",
    activebackground="#00cc88",
    padx=10,
    pady=5,
    command=close_window,
    relief="flat"
)
close_btn.pack(pady=30)

root.mainloop()