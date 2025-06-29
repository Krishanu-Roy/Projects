import re
import tkinter as tk
from tkinter import messagebox, ttk

import requests
from auth import check_login_status, logout_user, show_login_form


def luhn_check(card_number):
    digits = [int(d) for d in str(card_number) if d.isdigit()]
    checksum = 0
    parity = len(digits) % 2
    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0

def validate_email(email):
    API_KEY = "************************************"
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get("deliverability") == "DELIVERABLE"
    except Exception:
        return False

def validate_aadhaar(aadhaar):
    return aadhaar.isdigit() and len(aadhaar) == 12

def validate_pan(pan):
    return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan))

def assess_credit(name, income, credit_score, education, requested_amount):
    education_scores = {'Bachelors': 1, 'Masters': 1.2, 'HighSchool': 0.5}
    edu_score = education_scores.get(education, 0.5)
    risk_score = 0.5 * (credit_score / 850) + 0.3 * (income / 100000) + 0.2 * edu_score

    if risk_score > 0.8:
        max_credit = 20000
        interest = 5
    elif risk_score > 0.6:
        max_credit = 10000
        interest = 10
    else:
        max_credit = 0
        interest = None

    if max_credit == 0:
        return f"Sorry {name}, your credit card application is declined."
    elif requested_amount > max_credit:
        return (f"Hi {name}, you are approved for a credit card up to ${max_credit} at {interest}% interest.\n"
                f"Requested amount exceeds your limit. Please request ${max_credit} or less.")
    else:
        return (f"Congratulations {name}!\n"
                f"You are approved for a credit card with a limit of ${requested_amount} at {interest}% interest.")

def run_credit_card_app():
    if not check_login_status():
        root = tk.Tk()
        root.withdraw()
        show_login_form(root, run_credit_card_app)
        root.mainloop()
        return

    def on_submit():
        name = name_var.get()
        email = email_var.get()
        aadhaar = aadhaar_var.get()
        pan = pan_var.get()
        try:
            income = float(income_var.get())
            credit_score = int(credit_score_var.get())
            education = education_var.get()
            requested_amount = float(requested_amount_var.get())
            card_number = card_number_var.get()

            if not validate_email(email):
                messagebox.showerror("Invalid Email", "The email address is not valid or not deliverable.")
                return
            if not validate_aadhaar(aadhaar):
                messagebox.showerror("Invalid Aadhaar", "Aadhaar number must be 12 digits.")
                return
            if not validate_pan(pan):
                messagebox.showerror("Invalid PAN", "PAN must be in format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F).")
                return
            if not luhn_check(card_number):
                messagebox.showerror("Invalid Card", "The card number is not valid (Luhn check failed).")
                return

            result = assess_credit(name, income, credit_score, education, requested_amount)
            messagebox.showinfo("Application Result", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Money Lending - Credit Card Application")
    root.geometry("480x570")
    root.configure(bg="#e9f0fb")

    outer_frame = tk.Frame(root, bg="#e9f0fb")
    outer_frame.pack(expand=True, fill=tk.BOTH)

    card = tk.Frame(outer_frame, bg="#ffffff", bd=0, relief=tk.FLAT)
    card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=410, height=520)

    header = tk.Canvas(card, width=410, height=70, bg="#4a90e2", highlightthickness=0)
    header.create_rectangle(0, 0, 410, 70, fill="#4a90e2", outline="")
    header.create_rectangle(0, 35, 410, 70, fill="#357abd", outline="")
    header.pack(fill=tk.X)
    header.create_text(205, 35, text="Money Lending Application", font=("Arial", 18, "bold"), fill="white")

    name_var = tk.StringVar()
    email_var = tk.StringVar()
    aadhaar_var = tk.StringVar()
    pan_var = tk.StringVar()
    income_var = tk.StringVar()
    credit_score_var = tk.StringVar()
    education_var = tk.StringVar()
    requested_amount_var = tk.StringVar()
    card_number_var = tk.StringVar()

    def add_row(label, var, row, is_combo=False, values=None):
        y = 90 + row * 42
        tk.Label(card, text=label, font=("Arial", 11, "bold"), bg="#ffffff", fg="#333").place(x=30, y=y)
        if is_combo:
            box = ttk.Combobox(card, textvariable=var, values=values, font=("Arial", 11), state="readonly")
            box.place(x=180, y=y, width=180)
        else:
            entry = ttk.Entry(card, textvariable=var, font=("Arial", 11))
            entry.place(x=180, y=y, width=180)
            def on_focus_in(event, e=entry):
                e.configure(style="Focus.TEntry")
            def on_focus_out(event, e=entry):
                e.configure(style="TEntry")
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

    add_row("Name:", name_var, 0)
    add_row("Email:", email_var, 1)
    add_row("Aadhaar:", aadhaar_var, 2)
    add_row("PAN:", pan_var, 3)
    add_row("Annual Income:", income_var, 4)
    add_row("Credit Score:", credit_score_var, 5)
    add_row("Education:", education_var, 6, is_combo=True, values=["Bachelors", "Masters", "HighSchool"])
    add_row("Requested Amount:", requested_amount_var, 7)
    add_row("Card Number:", card_number_var, 8)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Accent.TButton", font=("Arial", 13, "bold"), foreground="white", background="#4a90e2", borderwidth=0, focusthickness=3, focuscolor="#357abd")
    style.map("Accent.TButton", background=[("active", "#357abd")])
    style.configure("Focus.TEntry", fieldbackground="#e3f0ff")

    # --- Button Frame at the bottom of the card ---
    button_frame = tk.Frame(card, bg="#ffffff")
    button_frame.place(relx=0.5, rely=1.0, anchor="s", y=-20, width=320, height=80)

    logout_btn = ttk.Button(button_frame, text="Logout", command=logout_user, style="Accent.TButton")
    logout_btn.pack(side="top", pady=(0, 10), ipadx=10, ipady=4)

    apply_btn = ttk.Button(button_frame, text="Apply", command=on_submit, style="Accent.TButton")
    apply_btn.pack(side="top", ipadx=10, ipady=4)

    root.mainloop()
    

if __name__ == "__main__":
    run_credit_card_app()
