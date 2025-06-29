import tkinter as tk
from tkinter import messagebox

# Simulated user database
USER_DATABASE = {
    "user1": "password1",
    "user2": "password2"
}

class Auth:
    def __init__(self):
        self.logged_in = False

    def login(self, username, password):
        if username in USER_DATABASE and USER_DATABASE[username] == password:
            self.logged_in = True
            return True
        return False

    def logout(self):
        self.logged_in = False

auth = Auth()

def check_login_status():
    return auth.logged_in

def logout_user():
    auth.logout()
    messagebox.showinfo("Logout", "You have been logged out.")

def show_login_form(root, on_success):
    from tkinter import ttk

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("380x380")
    login_window.configure(bg="#e9f0fb")
    login_window.resizable(False, False)

    # Shadow effect
    shadow = tk.Frame(login_window, bg="#b0c4de")
    shadow.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=320, height=300, x=8, y=8)

    # Card frame (main container)
    card = tk.Frame(login_window, bg="white", bd=0, relief=tk.FLAT, highlightthickness=2, highlightbackground="#dbeafe")
    card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=320, height=300)

    # Gradient header
    header = tk.Canvas(card, width=320, height=70, bg="#4a90e2", highlightthickness=0)
    header.create_rectangle(0, 0, 320, 70, fill="#4a90e2", outline="")
    for i in range(70):
        color = f'#{74-i:02x}{144-i:02x}{226-i:02x}'
        header.create_line(0, i, 320, i, fill=color)
    header.create_text(160, 35, text="Welcome Back", font=("Segoe UI", 20, "bold"), fill="white")
    header.pack(fill=tk.X)

    # Username
    ttk.Style().configure("Modern.TEntry", font=("Segoe UI", 12))
    tk.Label(card, text="Username", font=("Segoe UI", 11, "bold"), bg="white", fg="#4a90e2").place(x=35, y=90)
    username_entry = ttk.Entry(card, font=("Segoe UI", 12), style="Modern.TEntry")
    username_entry.place(x=35, y=115, width=250, height=30)

    # Password
    tk.Label(card, text="Password", font=("Segoe UI", 11, "bold"), bg="white", fg="#4a90e2").place(x=35, y=155)
    password_entry = ttk.Entry(card, show="*", font=("Segoe UI", 12), style="Modern.TEntry")
    password_entry.place(x=35, y=180, width=250, height=30)

    # Button style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Accent.TButton", font=("Segoe UI", 13, "bold"), foreground="white", background="#4a90e2", borderwidth=0, focusthickness=3, focuscolor="#357abd", padding=6)
    style.map("Accent.TButton", background=[("active", "#357abd")])

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if auth.login(username, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            login_window.destroy()
            on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    
    ttk.Button(card, text="Login", command=attempt_login, style="Accent.TButton").place(x=100, y=230, width=120, height=38)

    # Optional: Focus on username entry
    username_entry.focus_set()