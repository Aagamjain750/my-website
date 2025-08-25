import os
import smtplib
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

# Load .env file
load_dotenv()

# Environment se email/password lena
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

app = Flask(__name__)
app.secret_key = "supersecretkey"  # session ke liye

otp_store = {}

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Project Form
@app.route('/project_form', methods=['GET', 'POST'])
def project_form():
    if request.method == 'POST':
        email = request.form['email']
        otp = str(random.randint(1000, 9999))
        otp_store[email] = otp

        # Send OTP
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, f"Your OTP is {otp}")
            server.quit()
        except Exception as e:
            return f"Error: {e}"

        session['email'] = email
        return redirect(url_for('otp_verify'))

    return render_template('project_form.html')

# OTP Verify
@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    email = session.get('email')
    if not email:
        return redirect(url_for('home'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if email in otp_store and otp_store[email] == entered_otp:
            return "✅ OTP Verified Successfully!"
        else:
            return "❌ Invalid OTP, try again."

    return render_template('otp_verify.html')


if __name__ == '__main__':
    app.run(debug=True)
