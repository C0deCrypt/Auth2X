import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import subprocess
import sv_ttk
from tkinter import filedialog

class VaultGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vault")
        self.root.geometry("1280x720")
        self.root.configure(bg="#0a0f1d")
        self.root.resizable(False, False)

        self.load_fonts()
        sv_ttk.set_theme("dark")
        self.create_widgets()

    def load_fonts(self):
        try:
            self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        except:
            self.title_font = font.Font(family="Helvetica", size=24, weight="bold")

        try:
            self.text_font = font.Font(family="Segoe UI", size=10)
            self.button_font = font.Font(family="Segoe UI", size=11, weight="bold")
        except:
            self.text_font = font.Font(family="Helvetica", size=10)
            self.button_font = font.Font(family="Helvetica", size=11, weight="bold")

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#0a0f1d", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(
            main_frame,
            text="🔐 YOUR SECRET VAULT",
            font=self.title_font,
            fg="#EDEBE8",
            bg="#0a0f1d"
        ).pack(anchor="w", pady=(0, 20))

        # File list
        columns = ("#1", "#2")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        self.tree.heading("#1", text="Filename")
        self.tree.heading("#2", text="Date Added")

        style = ttk.Style()
        style.configure("Treeview",
                        background="#1a1f35",
                        fieldbackground="#1a1f35",
                        foreground="#EDEBE8",
                        rowheight=28,
                        font=self.text_font)
        style.configure("Treeview.Heading", font=self.button_font, foreground="#42CC7E")
        style.map("Treeview", background=[("selected", "#42CC7E")])

        self.tree.pack(fill="both", expand=True)

        # File operation buttons
        btn_frame = tk.Frame(main_frame, bg="#0a0f1d")
        btn_frame.pack(fill="x", pady=(20, 0))

        self.create_button(btn_frame, "➕ Add File", self.add_file).pack(side="left", padx=10)
        self.create_button(btn_frame, "👁️ View File", self.view_file).pack(side="left", padx=10)
        self.create_button(btn_frame, "❌ Delete File", self.delete_file).pack(side="left", padx=10)

        # Footer
        tk.Label(
            main_frame,
            text="Every action requires re-authentication.",
            font=("Segoe UI", 8),
            fg="#A0A0C0",
            bg="#0a0f1d"
        ).pack(anchor="center", pady=10)

    def create_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#42CC7E",
            fg="#202342",
            font=self.button_font,
            bd=0,
            padx=10,
            pady=4,
            activebackground="#36B069",
            activeforeground="#0a0f1d",
            relief="flat",
            cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#4BDF8B"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#42CC7E"))
        return btn

    def add_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            self.tree.insert("", "end", values=(filename, "Just now"))
            messagebox.showinfo("Add File", f"File '{filename}' added to vault (simulated)")

    def view_file(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("View File", "Please select a file to view.")
            return
        filename = self.tree.item(selected[0])["values"][0]
        messagebox.showinfo("View File", f"Opening '{filename}' (simulated)")

    def delete_file(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete File", "Please select a file to delete.")
            return
        filename = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Delete File", f"Are you sure you want to delete '{filename}'?")
        if confirm:
            self.tree.delete(selected[0])
            messagebox.showinfo("Deleted", f"'{filename}' deleted from vault (simulated)")

if __name__ == "__main__":
    root = tk.Tk()
    if root.tk.call("tk", "windowingsystem") == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    app = VaultGUI(root)
    root.mainloop()
