"""
Run this alone to test if your Gmail email sending works,
without needing to run the whole Flask app or fill the contact form.

Usage:
    python test_email.py
"""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", GMAIL_USER)

print("---- Checking .env values ----")
print("GMAIL_USER:", GMAIL_USER)
print("NOTIFY_EMAIL:", NOTIFY_EMAIL)
print("GMAIL_APP_PASSWORD set:", bool(GMAIL_APP_PASSWORD))
if GMAIL_APP_PASSWORD:
    print("GMAIL_APP_PASSWORD length:", len(GMAIL_APP_PASSWORD),
          "(should be 16, no spaces)")
print()

if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    print("❌ GMAIL_USER or GMAIL_APP_PASSWORD is missing from your .env file.")
    print("   Open .env and make sure both are filled in, then run this again.")
    raise SystemExit(1)

msg = EmailMessage()
msg["Subject"] = "Test email from portfolio site"
msg["From"] = GMAIL_USER
msg["To"] = NOTIFY_EMAIL
msg.set_content("This is a test. If you're reading this in Gmail, SMTP is working correctly.")

print("---- Attempting to send ----")
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    print("✅ Sent successfully. Check your Gmail inbox (and Spam folder).")
except smtplib.SMTPAuthenticationError as e:
    print("❌ AUTHENTICATION FAILED.")
    print("   This almost always means one of these:")
    print("   1. You used your normal Gmail password instead of an App Password")
    print("   2. 2-Step Verification is not turned on for this Google account")
    print("   3. The App Password has a typo or extra space")
    print("   4. GMAIL_USER doesn't match the account the App Password was created for")
    print()
    print("   Fix: go to https://myaccount.google.com/apppasswords and generate")
    print("   a fresh app password, then paste it into .env with no spaces.")
    print()
    print("   Raw error:", e)
except smtplib.SMTPException as e:
    print("❌ SMTP error:", e)
except Exception as e:
    print("❌ Unexpected error:", type(e).__name__, "-", e)
