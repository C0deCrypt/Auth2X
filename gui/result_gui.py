import tkinter as tk

# ---------- Setup Main Window ----------
root = tk.Tk()
root.title("Login Successful")

# Define dimensions
window_width = 500
window_height = 600

# Center the window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#0a0f1d")  # Dark navy background
root.resizable(False, False)

# ---------- Define Colors & Fonts ----------
PRIMARY_COLOR = "#00ff99"   # Neon mint green
ACCENT_COLOR = "#1f2833"    # Dark grayish-black
FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SUBTEXT = ("Segoe UI", 14)
FONT_BUTTON = ("Segoe UI", 12, "bold")

# ---------- Main Frame to Center Content ----------
main_frame = tk.Frame(root, bg="#0a0f1d")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------- Title ----------
title_label = tk.Label(
    main_frame,
    text="✅ ACCESS GRANTED",
    font=FONT_TITLE,
    fg=PRIMARY_COLOR,
    bg="#0a0f1d",
    pady=10
)
title_label.pack(pady=(0, 20))

# ---------- Welcome Message ----------
msg_label = tk.Label(
    main_frame,
    text="Welcome to the system!",
    font=FONT_SUBTEXT,
    fg="#EDEBE8",
    bg="#0a0f1d"
)
msg_label.pack(pady=(0, 30))

# ---------- Close Button ----------
def close_window():
    root.destroy()

close_btn = tk.Button(
    main_frame,
    text="Close",
    font=FONT_BUTTON,
    bg=PRIMARY_COLOR,
    fg="#0a0f1d",
    activebackground="#00cc88",
    activeforeground="white",
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
    command=close_window
)
close_btn.pack()

# ---------- Run ----------
root.mainloop()
