# Credit Card Application System

A Python-based GUI application for credit card application and eligibility assessment, featuring user authentication, input validation, and a modern Tkinter interface.

---

## Features

- **User Authentication:** Secure login and logout system.
- **Modern GUI:** Clean, responsive interface built with Tkinter and ttk.
- **Input Validation:**
  - Email validation via AbstractAPI.
  - Aadhaar and PAN format checks.
  - Card number validation using the Luhn algorithm.
- **Credit Assessment:** Calculates eligibility, credit limit, and interest rate based on user data.
- **Result Feedback:** Displays approval/decline messages and credit details.
- **Logout Functionality:** Securely log out from the application.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/credit-card-app.git
   cd credit-card-app
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   > If `requirements.txt` is missing, install manually:
   ```sh
   pip install requests
   ```

---

## Usage

1. **Run the application:**
   ```sh
   python src/gui.py
   ```

2. **Login:**  
   Enter your credentials in the login window.

3. **Fill Application Form:**  
   Provide your name, email, Aadhaar, PAN, income, credit score, education, requested amount, and card number.

4. **Submit:**  
   Click "Apply" to validate your details and assess your credit eligibility.

5. **Logout:**  
   Use the "Logout" button to securely exit your session.

---

## Project Structure

```
credit-card-app/
│
├── src/
│   ├── gui.py         # Main GUI and application logic
│   └── auth.py        # Authentication functions
│
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Flow Chart

```text
[Start]
   |
   v
[Launch Application]
   |
   v
[Login Window]
   |
   |--(Valid Credentials?)--No-->[Show Error & Retry]
   |                |
   |               Yes
   v                |
[Show Main Application Form]
   |
   v
[User Inputs Details]
   |
   v
[Validate Inputs]
   |
   |--(Any Invalid?)--Yes-->[Show Error & Retry]
   |                |
   |               No
   v                |
[Assess Credit Eligibility]
   |
   v
[Show Result (Approved/Declined)]
   |
   v
[User can Logout or Exit]
   |
   v
[End]
```

---

## Notes

- **Email Validation:** Uses [AbstractAPI](https://www.abstractapi.com/email-verification-api) for email deliverability checks. Replace the API key in `gui.py` with your own for production use.
- **Aadhaar/PAN:** This app only checks format, not actual government databases.
- **Credit Assessment:** The logic is for demonstration and not for real financial decisions.

---

---

## Author
- Krishanu Roy
